from dagster import Definitions
from dagster_project.jobs import subscription_welcome_job

defs = Definitions(jobs=[subscription_welcome_job])
