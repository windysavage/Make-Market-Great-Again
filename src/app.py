import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import select
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response

from database.base import create_db_and_tables, get_session
from database.models import Subscriber
from utils import trigger_dagster_job

logging.basicConfig(
    level=logging.INFO,
    format=(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s'
    ),
    datefmt='%Y-%m-%d %H:%M:%S',
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='src/static'), name='static')

templates: Jinja2Templates = Jinja2Templates(directory='src/templates')
email_list: list[str] = []


class SubscribeResponse(BaseModel):
    message: str
    email: str
    is_success: bool = True


@app.get('/', response_class=HTMLResponse)
async def index(request: StarletteRequest) -> Response:
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/subscribe')
def subscribe(request: StarletteRequest, email: str = Form(...)) -> SubscribeResponse:
    with get_session() as session:
        existing = session.exec(
            select(Subscriber).where(Subscriber.email == email)
        ).first()
        if existing:
            return templates.TemplateResponse('subscribed.html', {'request': request})

        sub = Subscriber(email=email)
        session.add(sub)
        session.commit()
        session.refresh(sub)

    trigger_dagster_job(
        job_name='send_welcome_email_job',
        run_config={'ops': {'send_welcome_email_op': {'config': {'to_email': email}}}},
    )

    return templates.TemplateResponse('success.html', {'request': request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='0.0.0.0', port=8899, reload=False)
