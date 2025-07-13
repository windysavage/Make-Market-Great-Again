import logging
from collections.abc import Callable
from functools import wraps

from langchain.globals import set_debug
from langchain_community.callbacks import get_openai_callback

logger = logging.getLogger(__name__)


def llm_debug(
    enabled: bool = True,
) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """
    Decorator to wrap LLM calls with OpenAI callback for token/cost debug.
    """

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            if not enabled:
                return func(*args, **kwargs)

            set_debug(True)
            with get_openai_callback() as cb:
                result = func(*args, **kwargs)
                logger.info('\n🔍 [LLM Debug]')
                logger.info(f'  📦 Total tokens:     {cb.total_tokens}')
                logger.info(f'  🧠 Prompt tokens:    {cb.prompt_tokens}')
                logger.info(f'  📝 Completion tokens:{cb.completion_tokens}')
                logger.info(f'  💰 Total cost:       ${cb.total_cost:.5f}')
                return result

        return wrapper

    return decorator
