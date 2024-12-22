import asyncio

from apps.agent.src.core.tools import FetchUrlsTool, SummarizeTool

tool = SummarizeTool()
crawler = FetchUrlsTool()


async def main():
    data = await crawler.run(
        [
            "https://www.investing.com/equities/apple-computer-inc",
        ]
    )

    print(data)

    # summarized = await tool.run(data)
    # print(f"==>> summarized: {summarized}")


asyncio.run(main())
