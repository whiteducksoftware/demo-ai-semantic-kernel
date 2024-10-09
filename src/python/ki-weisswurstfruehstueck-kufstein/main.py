import asyncio

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.kernel import Kernel


# Define the agent name and instructions
AZURE_ASSISTANT_NAME = "AzureAssistant"
# INSTRUCTIONS = """
# You are an AI specialized in creating optimized, consistent names for Azure resources. Your task is to help users generate concise names that clearly identify the resource type, workload, environment, region, and unique identifier.

# Your goal:
# - Follow best practices for naming conventions.
# - Ensure names are brief, structured, and easy to manage.

# Ask for any missing details when needed and provide a single, refined name proposal based on the input. Minimize unnecessary explanations.




# """
INSTRUCTIONS = """
You are are asking for a name and age and if you have both information, you answer with the name and age of the person.
Sample:
This is Martin, he is 25 years old.

Important: If you already know the name, you only aks for the age and vice versa.

"""

async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory):
    print(f"User: '{input}'")
    async for content in agent.invoke(chat):
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        chat.add_message(content)

# https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming

async def main():
    # Create the instance of the Kernel
    kernel = Kernel()

    # Add the OpenAIChatCompletion AI Service to the Kernel
    kernel.add_service(AzureChatCompletion(service_id="agent"))

    # Create the agent
    agent = ChatCompletionAgent(service_id="agent", kernel=kernel, name=AZURE_ASSISTANT_NAME, instructions=INSTRUCTIONS)

    # Define the chat history
    chat = ChatHistory()

    chat.add_system_message(INSTRUCTIONS)

    # Respond to user input
    while True:
        user_input = input("User: ")
        await invoke_agent(agent, user_input, chat)


if __name__ == "__main__":
    asyncio.run(main())
