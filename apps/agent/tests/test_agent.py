import asyncio

from src.core.agents import FinBotAgent

agent = FinBotAgent()


async def test_agent():
    # Assuming `agent.chat` yields streaming responses
    async for response in agent.chat(
        user_message="Tôi nên đầu tư ra sao với 100m ? https://s.cafef.vn/lich-su-giao-dich-vnindex-1.chn; https://vn.investing.com/equities/vingroup-jsc-historical-data; https://vn.investing.com/equities/fpt-corp-historical-data. Tôi nên đầu tư cổ phiếu nào ?",
        stream=True,
        max_tokens=4096,
        temperature=0.8,
    ):
        print(response)


asyncio.run(test_agent())
