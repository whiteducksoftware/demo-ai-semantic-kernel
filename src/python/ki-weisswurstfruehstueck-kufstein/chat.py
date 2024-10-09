# Copyright (c) Microsoft. All rights reserved.

import asyncio

from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel
from SeoAgent import SeoAgent

###################################################################
# The following sample demonstrates how to create a simple,       #
# agent group chat that utilizes An Art Director Chat Completion  #
# Agent along with a Copy Writer Chat Completion Agent to         #
# complete a task.                                                #
###################################################################


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


REVIEWER_NAME = "SeoOptimizer"
REVIEWER_INSTRUCTIONS = """
You are an SEO optimizer with deep expertise in search engine algorithms and a focus on driving organic traffic. 
Your goal is to evaluate whether the provided content is optimized for SEO best practices. 
If the content meets standards, confirm that it is approved. 
If not, provide insights on how to improve SEO factors, without giving specific examples in a SINGLE proposal per respond. Focus on one point at a time. Keep it short!.
"""

# COPYWRITER_NAME = "CreativeBlogTitle"
# COPYWRITER_INSTRUCTIONS = """
# You are an expert blog title creator with a knack for crafting compelling and clickable titles. 
# Your goal is to generate a single, optimized blog title that captures the essence of the post while maximizing reader engagement. 
# Only provide one title per response. You're focused on clarity, creativity, and SEO impact. 
# Avoid unnecessary details or explanations. 
# Refine the title based on any suggestions provided
# """

COPYWRITER_NAME = "CreativeBlogTitle"
COPYWRITER_INSTRUCTIONS = """
You are a social media expert with a talent for creating compelling, clickable posts that capture attention and drive engagement. Your goal is to generate a single, optimized social media post that summarizes content effectively while maximizing reader interaction. Each post should be clear, creative, and impactful. Avoid unnecessary details or explanations. Refine the post based on any suggestions provided.
"""


def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(service_id=service_id))
    return kernel


async def main():
    # agent_reviewer = ChatCompletionAgent(
    #     service_id="artdirector",
    #     kernel=_create_kernel_with_chat_completion("artdirector"),
    #     name=REVIEWER_NAME,
    #     instructions=REVIEWER_INSTRUCTIONS,
    # )

    agent_seo = SeoAgent.create()
    agent_social = 

    agent_writer = ChatCompletionAgent(
        service_id="copywriter",
        kernel=_create_kernel_with_chat_completion("copywriter"),
        name=COPYWRITER_NAME,
        instructions=COPYWRITER_INSTRUCTIONS,
    )


    chat = AgentGroupChat(
        agents=[agent_writer, agent_reviewer],
        termination_strategy=ApprovalTerminationStrategy(agents=[agent_reviewer], maximum_iterations=15),
    )

    with open('blog.md', 'r',  encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    # input = "a slogan for a new line of electric cars."
    # input = "a title for a blog post that is about why you should migrate from .net 6 to .net 8"
    input = """
    find a good heading:
    """
    input = """
    Create a social media for the given blog post:
    """
    
    input += data

    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=input))
    print(f"# {AuthorRole.USER}: '{input}'")

    async for content in chat.invoke():
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")

    print(f"# IS COMPLETE: {chat.is_complete}")


if __name__ == "__main__":
    asyncio.run(main())
