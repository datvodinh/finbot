import asyncio

from apps.crawler import HtmlCrawler

crawler = HtmlCrawler(
    config={
        "fetch_strategy": "hybrid",
        "timeout": 30000,
        "end_with_capture": False,
    }
)


print(
    asyncio.run(
        crawler.run("https://github.com/matthewwithanm/python-markdownify")
        # crawler.run(
        #     "https://stackoverflow.com/questions/78902913/how-to-bypass-cloudflare-using-playwright"
        # )
    )
)
