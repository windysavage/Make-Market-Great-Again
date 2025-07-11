from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response

app: FastAPI = FastAPI()
app.mount('/static', StaticFiles(directory='src/static'), name='static')

templates: Jinja2Templates = Jinja2Templates(directory='src/templates')

email_list: list[str] = []


@app.get('/', response_class=HTMLResponse)
async def show_form(request: StarletteRequest) -> Response:
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/subscribe')
async def subscribe(email: str = Form(...)) -> Response:
    if email not in email_list:
        email_list.append(email)
        print(f'📬 收到新訂閱: {email}')
    return RedirectResponse('/', status_code=303)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='0.0.0.0', port=8888, reload=True)
