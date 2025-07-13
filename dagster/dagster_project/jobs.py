from dagster import job, op
from src.agent.agent import Agent
from src.utils import send_email


@op
def send_welcome_email_op() -> None:
    return send_email(
        to_email='water92001@gmail.com',
        subject='訂閱成功：追蹤川普發文對股市的潛在影響',
        body=(
            '感謝你訂閱 Make Market Great Again！🇺🇸📈\n\n'
            '我們會自動追蹤川普在 Truth Social 上的貼文，並透過 AI 模型即時分析其對特定股票（例如科技股、能源股等）的潛在短期影響。\n\n'  # noqa: E501
            '當我們偵測到具影響力的發文時，你將會收到通知。\n\n'
            '希望這項服務能幫助你更快掌握市場情緒，做出更有利的投資決策。\n\n'
            '如有任何回饋或建議，歡迎回信與我們聯繫！\n\n'
            '— Make Market Great Again 團隊'
        ),
    )


@op
def watch_trump_post_op() -> None:
    agent = Agent(target_username='realDonaldTrump', n_hours=1)
    agent.work()


@job
def send_welcome_email_job() -> None:
    send_welcome_email_op()


@job
def watch_trump_post_job() -> None:
    watch_trump_post_op()
