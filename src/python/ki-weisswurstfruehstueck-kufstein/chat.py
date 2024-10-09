import asyncio

from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from seo_boost_agent import SeoBoostAgent
from social_craft_agent import SocialCraftAgent


class ApprovalTerminationStrategy(TerminationStrategy):
    async def should_agent_terminate(self, agent, history):
        return "approved" in history[-1].content.lower()


async def main():

    agent_seo = SeoBoostAgent.create()
    agent_social = SocialCraftAgent.create()


    chat = AgentGroupChat(
        agents=[agent_seo, agent_social],
        termination_strategy=ApprovalTerminationStrategy(agents=[agent_seo], maximum_iterations=15),
    )

    with open('blog.md', 'r',  encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    input = f"Create a social media for the given blog post '{data}'"

    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=input))
    # print(f"# {AuthorRole.USER}: '{input}'")

    async for content in chat.invoke():
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        print('_' * 10) 

    print(f"# IS COMPLETE: {chat.is_complete}")


if __name__ == "__main__":
    asyncio.run(main())
