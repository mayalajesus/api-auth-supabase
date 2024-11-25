from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import Client, ClientOptions, create_client
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carregar variáveis de ambiente
load_dotenv()

# Configuração Supabase
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
PUBLIC_KEY: str = os.getenv("PUBLIC_KEY")
SERVICE_ROLE_KEY: str = os.getenv("SERVICE_ROLE_KEY")

# Inicializar os clientes
USER_CLIENT: Client = create_client(
    SUPABASE_URL,
    PUBLIC_KEY,
    options=ClientOptions(auto_refresh_token=False, persist_session=False)
)

ADMIN_CLIENT: Client = create_client(
    SUPABASE_URL,
    SERVICE_ROLE_KEY
)

app = FastAPI()

# Modelos para requisições
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str


@app.post("/signup")
async def signup(request: SignupRequest):
    try:
        # Criar usuário no Supabase
        response = USER_CLIENT.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        if response.user:
            logging.info(f"Novo usuário registrado: {response.user.email}")
            return {
                "message": "Conta criada com sucesso! Verifique seu e-mail para confirmação.",
                "user": {"email": response.user.email, "created_at": response.user.created_at}
            }

        raise HTTPException(status_code=400, detail="Erro desconhecido ao criar a conta")
    except Exception as e:
        logging.error(f"Erro ao criar conta: {e}")
        if "User already registered" in str(e):
            raise HTTPException(status_code=400, detail="E-mail já registrado")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.post("/login")
async def login(request: LoginRequest):
    try:
        response = USER_CLIENT.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        if response.user:
            logging.info(f"Usuário logado: {response.user.email}")
            return {"message": "Login realizado com sucesso!"}
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    except Exception as e:
        logging.error(f"Erro ao realizar login: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.post("/signout")
async def signout():
    try:
        USER_CLIENT.auth.sign_out()
        logging.info("Usuário saiu da conta com sucesso")
        return {"message": "Você saiu da conta com sucesso."}
    except Exception as e:
        logging.error(f"Erro ao realizar logout: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.get("/all_accounts")
async def all_emails():
    try:
        response = ADMIN_CLIENT.auth.admin.list_users()

        if response:
            # Filtrar e-mails válidos
            active_users = [
                {"email": user.email}
                for user in response
                if user.email and "@" in user.email  # Validação mínima
            ]
            return {"active_users": active_users}

        return {"message": "Nenhum usuário encontrado"}
    except Exception as e:
        logging.error(f"Erro ao listar contas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar contas")


@app.delete("/delete_account")
async def delete_account():
    try:
        user_response = USER_CLIENT.auth.get_user()

        if not user_response or not user_response.user:
            raise HTTPException(status_code=404, detail="Nenhum usuário logado encontrado")

        user_id = user_response.user.id
        ADMIN_CLIENT.auth.admin.delete_user(user_id, True)

        logging.info(f"Conta do usuário {user_response.user.email} deletada")
        return {
            "message": f"Conta do usuário {user_response.user.email} deletada com sucesso."
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logging.error(f"Erro ao excluir conta: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir conta")
