from datetime import UTC, datetime, timedelta

from dagster import OpExecutionContext, job, op
from src.agent.agent import Agent
from src.crawler import pull_user_post
from src.utils import send_email


@op(config_schema={'to_email': str})
def send_welcome_email_op(context: OpExecutionContext) -> None:
    to_email = context.op_config['to_email']
    return send_email(
        to_emails=[to_email],
        subject='📬 訂閱成功｜來自 Make Market Great Again 的即時市場監控服務',
        body=(
            'Hi，\n\n'
            '感謝你訂閱 Make Market Great Again！🇺🇸📈\n\n'
            '從現在起，我們的 AI Agent 將自動追蹤川普在 Truth Social 上的最新發言，'
            '並即時分析這些言論對美股（例如科技股、能源股、軍工股等）的潛在影響。\n\n'
            '📡 一旦偵測到具有市場影響力的發文，你將第一時間收到通知，'
            '協助你即時掌握投資風險與機會。\n\n'
            '這項服務的目標是協助你：\n'
            '- 快速掌握市場情緒\n'
            '- 預判潛在股價波動\n'
            '- 做出更有策略的投資決策\n\n'
            '如果你有任何回饋或想法，歡迎隨時回信與我們分享。\n\n'
            '祝你投資順利，\n'
            '— Make Market Great Again 團隊'
        ),
    )


@op
def watch_trump_post_op() -> None:
    posts = pull_user_post(
        username='realDonaldTrump',
        created_after=datetime.now(UTC) - timedelta(hours=1),
    )
    agent = Agent(target_username='realDonaldTrump')
    agent.work(posts=posts)


@job
def send_welcome_email_job() -> None:
    send_welcome_email_op()


@job
def watch_trump_post_job() -> None:
    watch_trump_post_op()
