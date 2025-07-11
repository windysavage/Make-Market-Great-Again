from dagster import Definitions
from dagster_project.jobs import hello_job

defs = Definitions(jobs=[hello_job])
