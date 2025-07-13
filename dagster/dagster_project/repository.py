from dagster import Definitions, ScheduleDefinition
from dagster_project.jobs import send_welcome_email_job, watch_trump_post_job

hourly_schedule = ScheduleDefinition(
    job=watch_trump_post_job,
    cron_schedule='0 * * * *',
    name='hourly_schedule',
)

defs = Definitions(
    jobs=[send_welcome_email_job, watch_trump_post_job], schedules=[hourly_schedule]
)
