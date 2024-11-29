import os
import time
import gradio as gr
from typing import Dict, List, Optional


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
        pass

    def build(self):
        with gr.Blocks(
            theme=gr.themes.Ocean(
                spacing_size=gr.themes.sizes.spacing_sm,
                radius_size=gr.themes.sizes.radius_xxl,
                text_size=gr.themes.sizes.text_md,
            ),
            css_paths=os.path.join(
                os.getcwd(),
                "src/gui/style/style.css",
            ),
            # fill_width=True,
            # fill_height=True,
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

            chatbot.clear(
                self._hello_message,
                outputs=[chatbot, history],
            )

            demo.load(
                self._hello_message,
                outputs=[chatbot, history],
            )

        return demo
