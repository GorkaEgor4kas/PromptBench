import time
import json
import asyncio
from openai import AsyncOpenAI


async def _call_one(
        name: str,
        client: AsyncOpenAI, 
        model: str,
        system_prompt: str,
        query: str
):
    #timer start
    start = time.time()

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.0
        )

        elapse = time.time() - start
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else 0

        #json parse try
        try:
            data = json.loads(content)
            tool = data.get("tool", "N/A")
            valid_json = "YES"
        except json.JSONDecodeError:
            tool = "N/A"
            valid_json = "NO"

        return {
            "model": name,
            "status": "ok",
            "latency": f"{elapse:.2f}s",
            "tokens": tokens,
            "tool": tool,
            "valid_json": valid_json,
            "raw": content
        }

    except Exception as e:
        elapse = time.time() - start        

        return {
            "model": model,
            "status": "error",
            "latency": f"{elapse:.2f}s",
            "tokens": 0,
            "tool": "N/A",
            "valid_json": "NO",
            "error": str(e)            
        }


async def run_all(
    clients: dict[str, dict],  # {name: {"client": AsyncOpenAI, "model": str}}
    prompt: str,
    query: str,
    times: int = 1,
    delay: float = 3.0
):
    
    all_results = []

    for name, cfg in clients.items():
        client = cfg["client"]
        model = cfg["model"]

        for _ in range(times):
            result = await _call_one(
                name=name,
                client=client,
                model=model,
                system_prompt=prompt,
                query=query
            )
            all_results.append(result)

            if times > 1:
                await asyncio.sleep(delay)

    return all_results
    


