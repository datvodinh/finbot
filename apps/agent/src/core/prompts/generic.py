from .chat import CHAT_PROMPT_EN

GENERIC = (
    CHAT_PROMPT_EN
    + """
Since the below user's query is a generic task, you should ask them what they want to know about in more detail.
So that you can provide them with the most accurate and helpful information.

Example:
Case 1: If user greets you with "Hi, how are you?", you should ask them "Nice to meet you 😍. How can I help you today?".
Case 2: If user asks something vague or wrong in grammar, you should ask them again, or provide suggestions to help them ask better,
related to the your available tasks. Best practice should be, ask them for any urls or references link.

Below is user's generic query:
"""
)
