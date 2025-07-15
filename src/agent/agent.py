import inspect
import logging

import attr
from langchain.chat_models import init_chat_model
from langchain_core.tools import BaseTool

import src.agent.tools as tools_module
from src.agent.prompt import post_analysis_prompt
from src.agent.utils import llm_debug
from src.crawler import Post

logger = logging.getLogger(__name__)


@attr.s()
class Agent:
    target_username: str = attr.ib()

    model_name: str = attr.ib(default='gpt-3.5-turbo')
    model_provider: str = attr.ib(default='openai')

    def __attrs_post_init__(self) -> None:
        self.model = init_chat_model(
            model=self.model_name, model_provider=self.model_provider
        ).bind_tools([tool for tool in self.tool_map.values()])

    @property
    def tool_map(self) -> dict[str, BaseTool]:
        return {
            obj.name: obj
            for _, obj in inspect.getmembers(tools_module)
            if isinstance(obj, BaseTool)
        }

    def generate_prompt(self, posts: list[Post]) -> str:
        post_texts = '\n\n'.join([f'- {post.content}' for post in posts])
        tool_descriptions = '\n'.join(
            f'- {tool_name}: {tool.description}'
            for tool_name, tool in self.tool_map.items()
        )

        return post_analysis_prompt.format_messages(
            username=self.target_username,
            tool_descriptions=tool_descriptions,
            post_texts=post_texts,
        )

    @llm_debug(enabled=True)
    def work(self, posts: list[Post]) -> None:
        if not posts:
            logger.info('There is no new post to be analyzed.')
            return

        prompt = self.generate_prompt(posts)
        result = self.model.invoke(input=prompt)

        for tool_call in result.tool_calls:
            tool_name = tool_call['name']
            args = tool_call['args']

            if tool_name in self.tool_map:
                tool_output = self.tool_map[tool_name].invoke(args)
                logger.info(f'✅ Called tool `{tool_name}` with result: {tool_output}')
            else:
                logger.info(f'⚠️ Tool `{tool_name}` not found.')


if __name__ == '__main__':
    # posts = pull_user_post(
    #     username='realDonaldTrump',
    #     created_after=datetime.now() - timedelta(hours=10),
    # )

    posts = [
        Post(
            content='我將取消所有電動車與AI產業的優惠，並且提高各國關稅',
            created_at='2025-01-01',
        )
    ]

    agent = Agent(target_username='realDonaldTrump')
    agent.work(posts=posts)
