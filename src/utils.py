import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from src.settings import get_settings

settings = get_settings()


def ensure_datetime_type(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError as e:
            raise ValueError(f'Invalid datetime string format: {value}') from e
    else:
        raise TypeError(f'Expected str or datetime, got {type(value).__name__}')

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))

    return dt


def send_email(to_emails: list[str], subject: str, body: str) -> None:
    """
    Sends a plain-text email to multiple recipients using BCC to protect privacy.

    Args:
        to_emails (List[str]): List of recipient email addresses (BCC).
        subject (str): Email subject line.
        body (str): Email body in plain text.

    Raises:
        smtplib.SMTPException: If there is an error sending the message.
    """
    msg = MIMEMultipart()
    msg['From'] = settings.FROM_EMAIL
    msg['Bcc'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg, from_addr=settings.FROM_EMAIL, to_addrs=to_emails)


def trigger_dagster_job(job_name: str, run_config: dict | None = None) -> dict:
    DAGSTER_URL = 'http://dagster-webserver:3000/graphql'
    query = """ mutation TriggerJob(
      $job: String!,
      $repo: String!,
      $location: String!,
      $config: RunConfigData
    ) {
      launchPipelineExecution(
        executionParams: {
          selector: {
            pipelineName: $job,
            repositoryName: $repo,
            repositoryLocationName: $location
          },
          runConfigData: $config
        }
      ) {
        __typename
        ... on LaunchPipelineRunSuccess {
          run {
            runId
          }
        }
        ... on PythonError {
          message
          stack
        }
      }
    }
"""
    response = requests.post(
        DAGSTER_URL,
        json={
            'query': query,
            'variables': {
                'job': job_name,
                'repo': '__repository__',
                'location': 'dagster_project.repository',
                'config': run_config or {},
            },
        },
    )
    return response.json()
