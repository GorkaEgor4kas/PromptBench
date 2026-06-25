from promptbench.display import show


def test_show_does_not_crash(capsys):
    results = [
        {
            "model": "TestModel",
            "status": "ok",
            "latency": "0.50s",
            "tokens": 100,
            "tool": "SEARCH",
            "valid_json": "YES",
            "raw": "{}"
        }
    ]
    show(results)
    captured = capsys.readouterr()
    assert "TestModel" in captured.out
    assert "SEARCH" in captured.out


def test_show_handles_error(capsys):
    results = [
        {
            "model": "BrokenModel",
            "status": "error",
            "latency": "0.10s",
            "tokens": 0,
            "tool": "N/A",
            "valid_json": "NO",
            "error": "Connection refused"
        }
    ]
    show(results, clean=False)
    captured = capsys.readouterr()
    assert "ERROR" in captured.out
    assert "Connection refused" in captured.out