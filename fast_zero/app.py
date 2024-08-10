from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

app.mount('/assets', StaticFiles(directory='fast_zero/assets'), name='assets')
app.mount('/static', StaticFiles(directory='fast_zero/static'), name='static')
templates = Jinja2Templates(directory='fast_zero/templates')

database = [
    {'id': 1, 'nome': 'batatinha', 'telefone': '92892828'},
    {'id': 2, 'nome': 'Serjão berranteiro', 'telefone': '0999909099'},
    {'id': 3, 'nome': 'Sonic the Hedgehog', 'telefone': '1231231456'},
    {'id': 4, 'nome': 'Tails', 'telefone': '92821736'},
]

class DataIn(BaseModel):
    nome: str
    telefone: str


class DataOut(BaseModel):
    id: int
    nome: str
    telefone: str

@app.get('/ping', status_code=HTTPStatus.OK, response_model=Message)
def ping():
    return {'message': 'pong'}


@app.get('/pinghtml', response_class=HTMLResponse)
async def pinghtml(request: Request):
    return templates.TemplateResponse(name='pong.html', request=request)


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        name='index.html',
        request=request,
        context={'data': database}
    )


@app.get('/data', response_model=list[DataOut])
def data():
    return database


@app.post('/cadastro')
def post_cadastro(data: DataIn):
    database.append(dict(id=len(database) + 1, **data.model_dump()))