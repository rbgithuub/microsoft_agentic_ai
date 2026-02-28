from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant")
user = UserProxyAgent(
    "user",
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
)

user.initiate_chat(
    assistant,
    message="Explain MongoDB indexing strategy"
)
