from .chat import CHAT_PROMPT_EN

RAG = (
    CHAT_PROMPT_EN
    + """
Below is some context (information) that you have to use to answer the user's questions.

--------------------------------------------
{context}
--------------------------------------------

Please note that, you are not allowed to make up any information outside of the context provided above. You still can give your
opinion or make some assumptions based on the context, but you must make it clear that it is your opinion or assumption.
"""
)
