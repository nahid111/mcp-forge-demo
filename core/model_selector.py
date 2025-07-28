from langchain_aws import ChatBedrock
from langchain_core.language_models import (
    LanguageModelLike,
)
from langchain_openai import ChatOpenAI

from core.settings import Settings


def get_langchain_model(settings: Settings = Settings()) -> LanguageModelLike:
    """
    Instantiate a model based on the USE_BEDROCK flag and available environment variables.
    Args:
        settings: Settings object containing environment variables.
    Returns:
        A ChatBedrock or ChatOpenAI model instance.
    Raises:
        ValueError: If no valid model configuration is found or required variables are missing.
    """

    if settings.USE_BEDROCK:
        if not all(
            [
                settings.BEDROCK_MODEL_NAME,
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY,
                settings.AWS_SESSION_TOKEN,
            ]
        ):
            raise ValueError(
                'Bedrock configuration incomplete. Ensure BEDROCK_MODEL_NAME, AWS_ACCESS_KEY_ID, '
                'AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN are set when USE_BEDROCK is true.'
            )
        try:
            return ChatBedrock(
                model_id=settings.BEDROCK_MODEL_NAME,
                temperature=0,
                beta_use_converse_api=False,
            )
        except Exception as e:
            raise ValueError(f'Failed to initialize ChatBedrock: {e}')

    # Default to OpenAI if USE_BEDROCK is False
    if settings.MODEL_NAME and settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model=settings.MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0,
        )

    # Raise an exception if no valid configuration is found
    raise ValueError(
        'No valid model configuration found. Set USE_BEDROCK=true with valid Bedrock credentials '
        '(BEDROCK_MODEL_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) or '
        'provide MODEL_NAME and OPENAI_API_KEY for OpenAI.'
    )


# Example usage
if __name__ == '__main__':
    try:
        model = get_langchain_model()
        print(f'Model instantiated: {type(model).__name__}')
        # Example interaction
        response = model.invoke('Hello, world!')
        print(response)
    except ValueError as e:
        print(f'Error: {e}')
