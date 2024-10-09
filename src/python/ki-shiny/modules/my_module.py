from shiny import module, ui

from core.di_container import DiContainer

welcome = ui.markdown(
    """
    Hi! I'm Book-Bot. I work with semantic-kernel and Azure OpenAi.
    Please make sure you have the following environment variables set:
    - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_TEXT_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_ENDPOINT`
    - `AZURE_OPENAI_API_KEY`
    """
)


@module.ui
def my_module_ui():
    return ui.div(
        ui.chat_ui("chat"),
        ui.output_text_verbatim("txt_output"),
    )


@module.server
def my_module_server(input, output, session, di_container: DiContainer):
    my_service = di_container.my_service

    chat = ui.Chat(id="chat", messages=[welcome])

    @chat.on_user_submit
    async def _():
        user = chat.user_input()
        response = await my_service.invoke_chat(user_input=user)

        await chat.append_message(f"{response}")
