from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis do Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

# Definindo o modelo de entrada para o login
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({"email": request.email, "password": request.password})
        if response.user:
            return {"message": "Login realizado com sucesso!"}
        else:
            raise HTTPException(status_code=400, detail="Credenciais inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")


def validate_password_strength(senha: str):
    # Expressão regular para validar a senha
    if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,}$', senha):
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter pelo menos 6 caracteres, incluindo uma letra maiúscula, uma letra minúscula e um caractere especial."
        )
@app.post("/signup")
async def signup(request: SignupRequest):
    try:
        # Valida a força da senha antes de enviar para o Supabase
        validate_password_strength(request.password)
        
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        # Verifica se a conta foi criada com sucesso
        if response.user:
            return {
                "message": "Conta criada com sucesso!",
                "user": {"email": response.user.email, "date": response.user.created_at}
            }
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar conta")
    except Exception as e:
        if "User already registered" in str(e):
            raise HTTPException(status_code=400, detail="Usuário já registrado com este e-mail")
        raise HTTPException(status_code=500, detail=f"Erro ao criar conta: {e}")
