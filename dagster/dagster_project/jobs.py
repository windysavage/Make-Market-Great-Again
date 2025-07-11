from dagster import job, op


@op
def say_hello() -> None:
    print('👋 Hello from Dagster!')


@job
def hello_job() -> None:
    say_hello()
