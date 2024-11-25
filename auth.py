from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
from supabase import ClientOptions, create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis do Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase = create_client(
  url, 
  key,
  options=ClientOptions(
    auto_refresh_token=False,
    persist_session=True,
  )
)

app = FastAPI()

# Definindo o modelo de entrada para o login
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

class DeleteRequest(BaseModel):
    email: str 


@app.post("/signup")
async def signup(request: SignupRequest):
    try:
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
    
@app.get("/all_accounts")
async def all_emails():
    try:
        # Obtém a lista de usuários
        response = supabase.auth.admin.list_users()

        # Verifica se a resposta contém usuários
        if response:
            # Extrair IDs e e-mails
            users_data = [
                {
                    "email": user.email
                }
                for user in response
            ]
            
            return {
                "message": "Lista de e-mails cadastrados",
                "users": users_data
            }
        else:
            return {
                "message": "Nenhum usuário encontrado",
                "users": []
            }
    except Exception as e:
        return {
            "message": "Erro ao listar usuários",
            "error": str(e)
        }
    

async def get_users():
    try:
        # Obtém a lista de usuários
        response = supabase.auth.admin.list_users()

        # Verifica se a resposta contém usuários
        if response:
            # Extrair IDs e e-mails
            users_data = [
                {
                    "id": user.id,
                    "email": user.email
                }
                for user in response
            ]
            
            return users_data
        else:
            return {
                "message": "Nenhum usuário encontrado",
                "users": []
            }
    except Exception as e:
        return {
            "message": "Erro ao listar usuários",
            "error": str(e)
        }    
    

@app.delete("/delete_account")
async def delete_account(request: DeleteRequest):
    try:
        # Obtém a lista de usuários
        users_data = get_users()

        # Verifica se houve erro ao listar usuários
        if isinstance(users_data, dict) and "error" in users_data:
            raise HTTPException(status_code=500, detail=users_data["error"])

        # Busca o ID do usuário pelo e-mail
        user_id_list = [user["id"] for user in users_data if user["email"] == request.email]

        if not user_id_list:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        user_id = user_id_list[0]

        # Exclui o usuário
        supabase.auth.admin.delete_user(user_id)

        return {
            "message": f"Conta do usuário com e-mail {request.email} deletada com sucesso."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir conta: {e}")