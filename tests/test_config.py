# tests/test_config.py
import os
from promptbench.config import load_llm_configs


def test_load_single_llm(monkeypatch):
    monkeypatch.setenv("LLM_1_NAME", "TestModel")
    monkeypatch.setenv("LLM_1_KEY", "sk-test")
    monkeypatch.setenv("LLM_1_BASE_URL", "https://api.test.com")
    monkeypatch.setenv("LLM_1_MODEL", "test-model-1")

    configs = load_llm_configs()
    assert len(configs) == 1
    assert configs[0].name == "TestModel"
    assert configs[0].key == "sk-test"
    assert configs[0].model == "test-model-1"


def test_load_multiple_llms(monkeypatch):
    monkeypatch.setenv("LLM_1_NAME", "Model1")
    monkeypatch.setenv("LLM_1_KEY", "key1")
    monkeypatch.setenv("LLM_2_NAME", "Model2")
    monkeypatch.setenv("LLM_2_KEY", "key2")
    monkeypatch.setenv("LLM_3_NAME", "") 

    configs = load_llm_configs()
    assert len(configs) == 2
    assert configs[0].name == "Model1"
    assert configs[1].name == "Model2"


def test_load_no_llms(monkeypatch):
    for key in list(os.environ.keys()):
        if key.startswith("LLM_"):
            monkeypatch.delenv(key, raising=False)

    configs = load_llm_configs()
    assert configs == []