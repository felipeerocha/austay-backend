# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega as configurações da aplicação a partir de variáveis de ambiente
    e do arquivo .env.
    """
    # Para o Pydantic-Settings encontrar o arquivo .env na raiz do projeto
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Variáveis que serão carregadas
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()