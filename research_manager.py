from agents import Runner, trace, gen_trace_id
from planner import planner_agent, WebSearchItem, WebSearchPlan
from writer import writer_agent, ReportData
from search import search_and_summarize
import asyncio
from dotenv import load_dotenv
load_dotenv()
class ResearchManager:

    async def run(self, query: str):
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")

            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     

            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."

            report = await self.write_report(query, search_results)
            yield "Report written, Displaying final report..."

            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        try:
            print(f"🔎 Searching for: {item.query}")
            summary = await asyncio.to_thread(search_and_summarize, item.query)
            return f"{item.query}\n\n{summary}"
        except Exception as e:
            print(f" Failed on: {item.query} → {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        print("Finished writing report")
        return result.final_output_as(ReportData)
