import ee
import os
import json
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

def authenticate_gee(env_path: str | None = None) -> None:
    """
    Autentica no Google Earth Engine usando o método moderno com Scopes explícitos.
    """
    # Tenta carregar variáveis de ambiente (se já não estiverem carregadas)
    if env_path and os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()

    # 1. Pega a chave do ambiente
    gee_key_content = os.getenv("GEE_PRIVATE_KEY_JSON")
    
    # Se não achou no env, verifica se o argumento passado foi o próprio conteúdo JSON
    # (Isso corrige um bug potencial onde o código original passava o JSON como 'env_path')
    if not gee_key_content and env_path and "private_key" in env_path:
        gee_key_content = env_path

    if not gee_key_content:
        # Tenta pegar da variável global do sistema se o .env falhou
        gee_key_content = os.environ.get("GEE_PRIVATE_KEY_JSON")
        if not gee_key_content:
             raise RuntimeError("ERRO CRÍTICO: Variável GEE_PRIVATE_KEY_JSON não encontrada no ambiente (.env).")

    # 2. Converte para Dicionário
    try:
        key_dict = json.loads(gee_key_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"O conteúdo de GEE_PRIVATE_KEY_JSON não é um JSON válido. Erro: {e}")

    # 3. Autentica com os ESCOPOS CORRETOS (A correção principal está aqui)
    try:
        SCOPES = ['https://www.googleapis.com/auth/earthengine']
        
        credentials = Credentials.from_service_account_info(
            key_dict, 
            scopes=SCOPES
        )
        
        ee.Initialize(credentials=credentials)
        
    except Exception as e:
        raise RuntimeError(f"Falha ao autenticar no Google Earth Engine. Detalhes: {e}")
# # wildfire_analyser/fire_assessment/auth.py

# import ee
# import os
# import json
# from dotenv import load_dotenv
# from tempfile import NamedTemporaryFile


# def authenticate_gee(env_path: str | None = None) -> None:
#     """
#     Authenticate Google Earth Engine using a service account JSON
#     stored in the GEE_PRIVATE_KEY_JSON environment variable.
#     """
#     if env_path:
#         load_dotenv(env_path)
#     else:
#         load_dotenv()

#     gee_key_json = os.getenv("GEE_PRIVATE_KEY_JSON")
#     if not gee_key_json:
#         raise RuntimeError("GEE_PRIVATE_KEY_JSON not found in environment")

#     try:
#         key_dict = json.loads(gee_key_json)
#     except json.JSONDecodeError as e:
#         raise ValueError("Invalid GEE_PRIVATE_KEY_JSON format") from e

#     try:
#         with NamedTemporaryFile(mode="w+", suffix=".json") as f:
#             json.dump(key_dict, f)
#             f.flush()
#             credentials = ee.ServiceAccountCredentials(
#                 key_dict["client_email"], f.name
#             )
#             ee.Initialize(credentials)
#     except Exception as e:
#         raise RuntimeError("Failed to authenticate with Google Earth Engine") from e
