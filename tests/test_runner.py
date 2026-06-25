import pytest
from unittest.mock import AsyncMock
from promptbench.runner import run_all


@pytest.mark.asyncio
async def test_run_calls_all_clients():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content='{"tool": "SEARCH"}'))],
        usage=AsyncMock(total_tokens=100)
    )

    clients = {
        "Model1": {"client": mock_client, "model": "m1"},
        "Model2": {"client": mock_client, "model": "m2"},
    }

    results = await run_all(clients, "system prompt", "test query", times=1)

    assert len(results) == 2
    assert results[0]["model"] == "Model1"
    assert results[1]["model"] == "Model2"
    assert mock_client.chat.completions.create.call_count == 2


@pytest.mark.asyncio
async def test_run_handles_error():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.side_effect = Exception("API error")

    clients = {
        "BrokenModel": {"client": mock_client, "model": "m1"},
    }

    results = await run_all(clients, "prompt", "query", times=1)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert "API error" in results[0]["error"]


@pytest.mark.asyncio
async def test_run_with_times():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="{}"))],
        usage=AsyncMock(total_tokens=50)
    )

    clients = {
        "Model1": {"client": mock_client, "model": "m1"},
    }

    results = await run_all(clients, "prompt", "query", times=3, delay=0)

    assert len(results) == 3
    assert all(r["model"] == "Model1" for r in results)