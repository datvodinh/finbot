import gradio as gr
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from src.gui.demo import FinbotGUI
from typing import List, Optional

app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    query: str = Field(
        ...,
        title="Query",
        description="The query to chat with the assistant.",
    )
    history: Optional[List[ChatMessage]] = Field(
        title="History",
        description="The chat history.",
    )


@app.get("/")
async def hello():
    return RedirectResponse(url="/v1/demo")


demo = (
    FinbotGUI()
    .build()
    .queue(
        api_open=False,
        default_concurrency_limit=16,
    )
)

gr.mount_gradio_app(
    app=app,
    blocks=demo,
    path="/v1/demo",
    root_path="/v1/demo",
    server_name="0.0.0.0",
    server_port=8000,
)

if __name__ == "__main__":
    uvicorn.run(
        "src.__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        reload_delay=0.5,
        use_colors=True,
    )
