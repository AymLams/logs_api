from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Logs API"
    data_folder: str
    max_file_size: int
    api_address: str
    api_port: int

    class Config:
        env_file = "config.json"

