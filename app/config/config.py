from dotenv import dotenv_values


env = dotenv_values()

def getenv(key, ntype, default=None):
    value = env.get(key)
    if not value:
        return default
    return ntype(value)


class Config:
    MAIN_BOT_TOKEN = getenv('TOKEN1', str)
    SUPPORT_BOT_TOKEN = getenv('TOKEN2', str)
    WORKER_BOT_TOKEN = getenv('TOKEN3', str)
