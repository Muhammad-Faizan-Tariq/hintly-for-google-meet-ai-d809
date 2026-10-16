import asyncio, json
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from ..llm_client import generate_hints

router = APIRouter(tags=["demo"])

DEMO_TRANSCRIPT = [
    {"speaker": "Sales Rep", "text": "Hi! Thanks for joining. I wanted to walk you through Hintly today."},
    {"speaker": "Prospect", "text": "Sure, we've been exploring AI tools for our sales calls."},
    {"speaker": "Sales Rep", "text": "Perfect. Hintly surfaces real-time suggestions so reps never miss a cue."},
    {"speaker": "Prospect", "text": "Interesting. What kind of suggestions does it give?"},
    {"speaker": "Sales Rep", "text": "Things like: ask about budget now, tone is too aggressive, or flag an action item."},
    {"speaker": "Prospect", "text": "We definitely lose track of follow-ups. That's a big pain point."},
    {"speaker": "Sales Rep", "text": "Hintly auto-generates action items and drafts your follow-up email before the call ends."},
    {"speaker": "Prospect", "text": "How does pricing work? We have around 20 reps."},
    {"speaker": "Sales Rep", "text": "For 20 seats, our Business plan is $15/user/month — $300 total. Includes all features."},
    {"speaker": "Prospect", "text": "Can we do a trial first before committing?"},
    {"speaker": "Sales Rep", "text": "Absolutely — 14-day free trial, up to 5 users, full feature access. No credit card needed."},
    {"speaker": "Prospect", "text": "That sounds great. Let's get started."},
]


@router.get("/api/demo/stream")
async def demo_stream():
    async def event_gen():
        window: list[dict] = []
        for i, chunk in enumerate(DEMO_TRANSCRIPT):
            window.append(chunk)
            yield {"event": "transcript", "data": json.dumps(chunk)}
            if (i + 1) % 3 == 0:
                hints = await generate_hints(window[-6:])
                for h in hints:
                    yield {"event": "hint", "data": json.dumps(h)}
            await asyncio.sleep(2)
        yield {"event": "done", "data": json.dumps({"message": "Demo complete"})}

    return EventSourceResponse(event_gen())
