import logging
from collections.abc import AsyncGenerator
from typing import Any

import aiohttp
from pydantic import HttpUrl

from kaito.kaito_prompt_execution_settings import KaitoTextPromptExecutionSettings
from kaito.utils import AsyncSession
from semantic_kernel.connectors.ai.text_completion_client_base import TextCompletionClientBase
from semantic_kernel.contents.streaming_text_content import StreamingTextContent
from semantic_kernel.contents.text_content import TextContent

logger: logging.Logger = logging.getLogger(__name__)


class KaitoTextCompletion(TextCompletionClientBase):
    """Initializes a new instance of the KaitoTextCompletion class.

    Make sure to have the kaito service running either locally or remotely.

    Args:
        ai_model_id (str): kaito model name, see https://kaito.ai/library
        url (Optional[Union[str, HttpUrl]]): URL of the kaito server, defaults to http://localhost:11434/api/chat
        session (Optional[aiohttp.ClientSession]): Optional client session to use for requests.
    """

    url: HttpUrl = "http://localhost:11434/api/chat"
    session: aiohttp.ClientSession | None = None

    
    async def get_text_contents(
        self,
        prompt: str,
        settings: KaitoTextPromptExecutionSettings,
    ) -> list[TextContent]:
        """This method is invoked by the kernel to retrieve a response from a text-optimized LLM.

        Parameters:
            prompt (str): The input prompt to be completed.
            settings (KaitoTextPromptExecutionSettings): Configuration settings for the execution.

        Returns:
            List["TextContent"]: The list of generated text completions.
        """
        if not settings.ai_model_id:
            settings.ai_model_id = self.ai_model_id

        settings.prompt = prompt
        settings.return_full_text = False
        settings.stream = False
        settings.generate_kwargs = {"max_length": 1000}
        async with (
            AsyncSession(self.session) as session,
            session.post(str(self.url), json=settings.prepare_settings_dict()) as response,
        ):
            response.raise_for_status()
            response_object = await response.json()
            text = response_object['Result']
            return [
                TextContent(
                    inner_content=response_object,
                    ai_model_id=self.ai_model_id,
                    text=text
                )
            ]

    async def get_streaming_text_contents(
        self,
        prompt: str,
        settings: KaitoTextPromptExecutionSettings,
    ) -> AsyncGenerator[list[StreamingTextContent], Any]:
        pass

    def get_prompt_execution_settings_class(self) -> "KaitoTextPromptExecutionSettings":
        """Get the request settings class."""
        return KaitoTextPromptExecutionSettings
