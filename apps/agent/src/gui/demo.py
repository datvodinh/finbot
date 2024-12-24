import os
import time
from typing import Dict, List, Optional

import gradio as gr

from src.core.agents import FinBotAgent

agent = FinBotAgent()


class FinbotGUI:
    def _hello_message(self):
        message = "Hi 👋! Mình là Finbot, mình có thể giúp gì được cho bạn?"
        for i in range(len(message)):
            time.sleep(0.01)

            yield (
                [
                    {
                        "role": "assistant",
                        "content": message[: i + 1],
                    }
                ],
                [],
            )

    def _update_history(
        self,
        message: str,
        chatbot: List[Dict[str, str]],
        history: Optional[List[Dict[str, str]]] = None,
    ):
        assistant = chatbot[-1]
        assistant.pop("metadata", None)
        messages = [
            {
                "role": "user",
                "content": message["text"],
            },
            chatbot[-1],
        ]
        history.extend(messages)

        return "", history

    async def _query(
        self,
        message: str,
        chatbot: List[Dict[str, str]],
        history: Optional[List[Dict[str, str]]] = None,
    ):
        query = message["text"]
        chatbot.append(
            {
                "role": "user",
                "content": query,
            }
        )

        async for response in agent.chat(
            user_message=message["text"],
            stream=True,
            history=history[-5:],
            max_completion_tokens=4000,
            temperature=0.5,
        ):
            all_reponse = ""

            if response["action"] == "task_check":
                message = [
                    {
                        "role": "assistant",
                        "content": response["content"].upper(),
                        "metadata": {
                            "title": f"🤔 Task: {response['content'].upper()}"
                        },
                    }
                ]

                chatbot.extend(message)

                yield chatbot
            elif response["action"] == "search_urls":
                message = [
                    {
                        "role": "assistant",
                        "content": "\n ".join(response["content"]),
                        "metadata": {
                            "title": "🔍 Search URLs.",
                        },
                    }
                ]
                chatbot.extend(message)

                yield chatbot

            elif response["action"] == "fetch_urls":
                message = [
                    {
                        "role": "assistant",
                        "content": "\n ".join(response["content"]),
                        "metadata": {
                            "title": "🔗 Found URLs, fetching contents ...",
                        },
                    }
                ]
                chatbot.extend(message)

                yield chatbot
            elif response["action"] in ["crawl_urls", "search"]:
                message = [
                    {
                        "role": "assistant",
                        "content": "",
                        "metadata": {
                            "title": response["content"],
                        },
                    }
                ]
                chatbot.extend(message)

                yield chatbot
            elif response["action"] == "vector_store":
                message = [
                    {
                        "role": "assistant",
                        "content": response["content"],
                        "metadata": {
                            "title": "📦 Stored in QDrant!",
                        },
                    }
                ]
                chatbot.extend(message)

                yield chatbot
            elif response["action"] == "answer":
                async for chunk in response["content"]:
                    all_reponse += chunk.choices[0].delta.content or ""
                    messages = [
                        {
                            "role": "assistant",
                            "content": all_reponse,
                        }
                    ]

                    yield chatbot + messages
            else:
                raise ValueError(f"Unknown action: {response['action']}")

    def build(self):
        with gr.Blocks(
            theme=gr.themes.Ocean(),
            css_paths=os.path.join(
                os.getcwd(),
                "apps/agent/src/gui/style/style.css",
            ),
        ) as demo:
            gr.Markdown(
                "## Finbot",
                elem_classes=["centered-markdown"],
                elem_id="centered-markdown",
            )
            with gr.Row(show_progress=False):
                with gr.Column(scale=4, variant="panel"):
                    chatbot = gr.Chatbot(
                        type="messages",
                        height="69vh",
                        label="Finbot",
                        bubble_full_width=False,
                    )
                    history = gr.State([])
                    answer = gr.State("")
                    with gr.Row():
                        message = gr.MultimodalTextbox(
                            show_label=False,
                            file_types=["text"],
                            placeholder="Nhập tin nhắn của bạn ở đây",
                            scale=10,
                        )

            message.submit(
                self._query,
                inputs=[message, chatbot, history],
                outputs=[chatbot],
            ).then(
                self._update_history,
                inputs=[message, chatbot, history],
                outputs=[message, history],
            ).then(
                lambda x: None,
                inputs=[answer],
                outputs=[answer],
            )

            chatbot.clear(
                self._hello_message,
                outputs=[chatbot, history],
            )

            demo.load(
                self._hello_message,
                outputs=[chatbot, history],
            )

        return demo
