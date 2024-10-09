from typing import Any, Literal
from pydantic import Field
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings


class KaitoPromptExecutionSettings(PromptExecutionSettings):
    ai_model_id: str = Field("", serialization_alias="model")
    format: Literal["json"] | None = None
    options: dict[str, Any] | None = None
    stream: bool = False


class KaitoTextPromptExecutionSettings(KaitoPromptExecutionSettings):
    prompt: str | None = None
    return_full_text: bool = False
    generate_kwargs: dict[str, Any] | None = None
