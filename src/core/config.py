from os import getenv
#DB_CONFIG = f"postgresql+asyncpg://postgres:qwerty@localhost:5432/finance"

class Setting():
    db_url: str = f"postgresql+asyncpg://postgres:qwerty@localhost:5432/finance"
    db_echo: bool = True


settings = Setting()
