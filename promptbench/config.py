import os 
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMConfig(BaseModel):
    name: str
    key: str
    base_url: str
    model: str

def load_llm_config() -> list[LLMConfig]:
    """
    Loads all LLM_* variables from .env and returns a list of configs
    """

    configs = []
    i = 1 

    while True:
        name = os.getenv(f"LLM_{i}_NAME")
        if not name:
            break

        configs.append(LLMConfig(
            name = name,
            key = os.getenv(f"LLM_{i}_KEY", ""),
            base_url = os.getenv(f"LLM_{i}_BASE_URL", "https://api.openai.com/v1"),
            model = os.getenv(f"LLM_{i}_MODEL", "")
        ))
        i += 1

    return configs

def create_clients(configs: list[LLMConfig]) -> dict[str, AsyncOpenAI]:
    """
    Creates clients for each config 
    """
    return {
        cfg.name: {
            "client": AsyncOpenAI(api_key=cfg.key, base_url=cfg.base_url),
            "model": cfg.model
        }
        for cfg in configs
    }
