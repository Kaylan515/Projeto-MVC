from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

templates = Jinja2Templates(directory="app/templates")

#Rota de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request})

@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request})

# Criar o usuario no banco
@router.post("/cadastro")
def cadastrar_user(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    #Verificar se o email está cadatrado
    user_existente = db.query(Usuario).filter_by(email=email).first()
    if user_existente:
        # Retorna o formulário com mensagem de erro
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            {"request": request, "erro": "Este e-mail já está cadastrado."}
        )
    
    #Criar o novo usuário com senha hash
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha), #Nunca salva a senha pura no db
        )
    
    db.add(novo_usuario)
    db.commit()

    #Redirecionar para login após cadastro
    return RedirectResponse(url="/auth/login?cadastro=ok", status_code=302)