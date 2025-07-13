from dagster import Definitions
from dagster_project.jobs import send_welcome_email_job, watch_trump_post_job

defs = Definitions(jobs=[send_welcome_email_job, watch_trump_post_job])
