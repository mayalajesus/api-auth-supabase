from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import Client, ClientOptions, create_client

# Carregar variáveis de ambiente
load_dotenv()

# Configuração Supabase
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
PUBLIC_KEY: str = os.getenv("PUBLIC_KEY")  # Chave pública
SERVICE_ROLE_KEY: str = os.getenv("SERVICE_ROLE_KEY")  # Chave administrativa

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
        response = USER_CLIENT.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
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


@app.post("/login")
async def login(request: LoginRequest):
    try:
        response = USER_CLIENT.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        if response.user:
            return {"message": "Login realizado com sucesso!"}
        else:
            raise HTTPException(status_code=400, detail="Credenciais inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")


@app.post("/signout")
async def signout():
    try:
        USER_CLIENT.auth.sign_out()
        return {"message": "Você saiu da conta com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")


@app.get("/all_accounts")
async def all_emails():
    try:
        # Usando a API Admin para listar todos os usuários
        response = ADMIN_CLIENT.auth.admin.list_users()

        if response:
            # Filtrar e-mails que não são strings aleatórias
            active_users = [
                {"email": user.email}
                for user in response
                if user.email and "@" in user.email  # Garante que é um e-mail válido
            ]
            return {"active_users": active_users}
        else:
            return {"message": "Nenhum usuário encontrado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar contas: {e}")


@app.delete("/delete_account")
async def delete_account():
    try:
        # Obter o usuário logado
        user_response = USER_CLIENT.auth.get_user()

        if not user_response or not user_response.user:
            raise HTTPException(status_code=404, detail="Nenhum usuário logado encontrado")

        user_id = user_response.user.id  # Obter o ID do usuário logado

        # Usar o cliente administrativo para deletar o usuário
        ADMIN_CLIENT.auth.admin.delete_user(user_id, True)

        return {
            "message": f"Conta do usuário {user_response.user.email} deletada com sucesso."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir conta: {e}")