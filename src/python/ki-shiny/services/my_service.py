from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import PromptTemplateConfig
from semantic_kernel.prompt_template.input_variable import InputVariable

from core.logging import log_function_call

welcome = """
    Hi! I'm Book-Bot. I work with semantic-kernel and Azure OpenAi.
    Please make sure you have the following environment variables set:
    - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_TEXT_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_ENDPOINT`
    - `AZURE_OPENAI_API_KEY`
    """


prompt = """
ChatBot can have a conversation with you about any topic.
It can give explicit instructions or say 'I don't know' if it does not have an answer.

{{$history}}
User: {{$user_input}}
ChatBot: """


class MyService:
    def __init__(self, config_service):
        self.kernel = Kernel()
        self.chat_history = ChatHistory()
        self.chat_history.add_system_message(
            "You are a helpful chatbot who is good about giving book recommendations."
        )
        self.prompt = prompt
        self.kernel.add_service(
            AzureChatCompletion(service_id="chat-gpt", env_file_path=".env")
        )
        self.settings = self.kernel.get_prompt_execution_settings_from_service_id(
            "chat-gpt"
        )
        self.settings.max_tokens = 2000  # type: ignore
        self.settings.temperature = 0.7  # type: ignore
        self.settings.top_p = 0.8  # type: ignore
        self.prompt_template_config = PromptTemplateConfig(
            template=prompt,
            name="chat",
            template_format="semantic-kernel",
            input_variables=[
                InputVariable(
                    name="user_input", description="The user input", is_required=True
                ),
                InputVariable(
                    name="history",
                    description="The conversation history",
                    is_required=True,
                ),
            ],
            execution_settings=self.settings,  # type: ignore
        )

        self.chat_function = self.kernel.add_function(
            function_name="chat",
            plugin_name="chatPlugin",
            prompt_template_config=self.prompt_template_config,
        )

    @log_function_call(log_level="info")
    async def invoke_chat(self, user_input, history=None):
        if history is None:
            history = self.chat_history
        arguments = KernelArguments(user_input=user_input, history=history)
        response = await self.kernel.invoke(self.chat_function, arguments)  # type: ignore
        self.chat_history.add_user_message(user_input)
        return response
