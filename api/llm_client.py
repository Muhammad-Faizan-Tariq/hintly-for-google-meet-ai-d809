import os, asyncio, json
from openai import AsyncOpenAI

_client = AsyncOpenAI(
    api_key=os.getenv("NVIDIA_API_KEY", ""),
    base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
    timeout=300.0,
)
MODEL = os.getenv("NVIDIA_MODEL", "nvidia/kimi-k2-instruct")


async def complete_text(prompt: str) -> str:
    for attempt in range(2):
        try:
            resp = await _client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt == 0:
                await asyncio.sleep(60)
            else:
                raise e
    return ""


async def generate_hints(transcript_window: list[dict]) -> list[dict]:
    lines = "\n".join(f"{t['speaker']}: {t['text']}" for t in transcript_window[-12:])
    prompt = (
        "Analyze this meeting transcript and return 1-3 real-time AI hints.\n\n"
        f"Transcript:\n{lines[:3000]}\n\n"
        'Return ONLY a JSON array. Each hint: {"type":"suggestion|action_item|tone|question","text":"...","confidence":0.0-1.0}'
    )
    raw = await complete_text(prompt)
    try:
        s, e = raw.find("["), raw.rfind("]") + 1
        return json.loads(raw[s:e]) if s >= 0 else []
    except Exception:
        return []


async def generate_summary(transcript: list[dict], title: str) -> dict:
    lines = "\n".join(f"{t['speaker']}: {t['text']}" for t in transcript[-40:])
    prompt = (
        f'Meeting: "{title}"\n\nTranscript:\n{lines[:5000]}\n\n'
        'Return ONLY JSON: {"summary":"...","action_items":["..."],"follow_up_email":"..."}'
    )
    raw = await complete_text(prompt)
    try:
        s, e = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[s:e]) if s >= 0 else {}
    except Exception:
        return {"summary": "Summary unavailable", "action_items": [], "follow_up_email": ""}
