import inspect
from datetime import datetime, timedelta

import attr
import tools as tools_module
from langchain.chat_models import init_chat_model
from prompt import post_analysis_prompt

from src.crawler import Post, pull_user_post
from utils import llm_debug


@attr.s()
class Agent:
    target_username: str = attr.ib()
    n_hours: int = attr.ib()

    model_name: str = attr.ib(default='gpt-3.5-turbo')
    model_provider: str = attr.ib(default='openai')

    def __attrs_post_init__(self) -> None:
        self.model = init_chat_model(
            model=self.model_name, model_provider=self.model_provider
        ).bind_tools(self.tool_list)

    @property
    def tool_list(self) -> list[callable]:
        return [
            fn
            for _, fn in inspect.getmembers(tools_module, inspect.isfunction)
            if getattr(fn, '__tool__', False)
        ]

    def crawl(self) -> list[Post]:
        return pull_user_post(
            username=self.target_username,
            created_after=datetime.now() - timedelta(hours=self.n_hours),
        )

    def generate_prompt(self, posts: list[Post]) -> str:
        post_texts = '\n\n'.join([f'- {post.content}' for post in posts])
        return post_analysis_prompt.format_messages(
            username=self.target_username, post_texts=post_texts
        )

    @llm_debug(enabled=False)
    def work(self) -> None:
        posts = self.crawl()
        prompt = self.generate_prompt(posts)
        return self.model.invoke(input=prompt)


if __name__ == '__main__':
    agent = Agent(target_username='realDonaldTrump', n_hours=1)
    agent.work()
