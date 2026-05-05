from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.controllers import auth_controller

app = FastAPI(title="Sistema de estoque")

#Configurar o fastapi para serivir os arquivos estáticos (CSS, JS, Imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

#Incluir os routers dos controles
app.include_router(auth_controller.router)