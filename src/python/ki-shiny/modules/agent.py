# Copyright (c) Microsoft. All rights reserved.

import asyncio
import random

from loguru import logger
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import (
    TerminationStrategy,
)
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel
from shiny import module, ui

from core.di_container import DiContainer

welcome = ui.markdown(
    """
    Please provide a blog post. I will think up a title for it,
    and then we will have an SEO expert review it." 
    """
)


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


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


@module.ui
def agent_ui():
    return ui.div(
        ui.chat_ui("chat"),
        ui.output_text_verbatim("txt_output"),
    )



@module.server
def agent_server(input, output, session, di_container: DiContainer):
    my_service = di_container.my_service


    chat = ui.Chat(
        id="chat",
        messages=[welcome],
    )

    def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
        kernel = Kernel()
        kernel.add_service(AzureChatCompletion(service_id=service_id))
        return kernel

    agent_reviewer = ChatCompletionAgent(
        service_id="artdirector",
        kernel=_create_kernel_with_chat_completion("artdirector"),
        name=REVIEWER_NAME,
        instructions=REVIEWER_INSTRUCTIONS,
    )

    agent_writer = ChatCompletionAgent(
        service_id="copywriter",
        kernel=_create_kernel_with_chat_completion("copywriter"),
        name=COPYWRITER_NAME,
        instructions=COPYWRITER_INSTRUCTIONS,
    )

    agent_chat = AgentGroupChat(
        agents=[agent_writer, agent_reviewer],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[agent_reviewer], maximum_iterations=10
        ),
    )

    @chat.on_user_submit
    async def _():
        user = chat.user_input()
        await agent_chat.add_chat_message(
            ChatMessageContent(role=AuthorRole.USER, content=user)  # type: ignore
        )

        async for content in agent_chat.invoke():
            agent_text = f"{content.role} - {content.name or '*'}: '{content.content}'"

            if "CreativeBlogTitle" in agent_text:
                chat_msg = {
                    "content": f"{content.content}",
                    "role": "assistant",
                }
            else:
                chat_msg = {
                    "content": f"{content.content}",
                    "role": "user",
                }
            await chat.append_message(chat_msg)
            # await asyncio.sleep(random.uniform(0.5, 1.5))
