import uuid, asyncio, json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sse_starlette.sse import EventSourceResponse
from ..database import get_db, SessionLocal
from ..models import Meeting, Transcript, Hint, User, MeetingCreate, TranscriptChunk, MeetingOut, HintOut
from ..auth_utils import get_current_user
from ..llm_client import generate_hints, generate_summary

router = APIRouter(prefix="/api/meetings", tags=["meetings"])


async def _get_meeting(mid: str, uid: str, db: AsyncSession) -> Meeting:
    r = await db.execute(select(Meeting).where(Meeting.id == mid, Meeting.user_id == uid))
    m = r.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return m


@router.post("", response_model=MeetingOut)
async def create_meeting(body: MeetingCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    m = Meeting(id=str(uuid.uuid4()), user_id=user.id, google_meet_id=body.meeting_id, title=body.title)
    db.add(m); await db.commit(); await db.refresh(m)
    return MeetingOut.model_validate(m)


@router.post("/{mid}/transcript")
async def add_transcript(mid: str, body: TranscriptChunk, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _get_meeting(mid, user.id, db)
    db.add(Transcript(id=str(uuid.uuid4()), meeting_id=mid, speaker=body.speaker, text=body.text, ts=body.ts))
    await db.commit()
    return {"status": "ok"}


@router.get("/{mid}/hints/stream")
async def hints_stream(mid: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _get_meeting(mid, user.id, db)

    async def event_gen():
        async with SessionLocal() as gen_db:
            while True:
                r_m = await gen_db.execute(select(Meeting).where(Meeting.id == mid))
                meeting = r_m.scalar_one_or_none()
                if meeting and meeting.ended_at:
                    yield {"event": "ended", "data": json.dumps({"message": "Meeting ended"})}
                    break
                r = await gen_db.execute(
                    select(Transcript).where(Transcript.meeting_id == mid)
                    .order_by(Transcript.ts.desc()).limit(12)
                )
                chunks = [{"speaker": t.speaker, "text": t.text} for t in reversed(r.scalars().all())]
                if chunks:
                    hints = await generate_hints(chunks)
                    for h in hints:
                        gen_db.add(Hint(id=str(uuid.uuid4()), meeting_id=mid,
                                        type=h.get("type", "suggestion"), text=h.get("text", ""),
                                        confidence=float(h.get("confidence", 0.8))))
                    await gen_db.commit()
                    for h in hints:
                        yield {"event": "hint", "data": json.dumps(h)}
                await asyncio.sleep(5)

    return EventSourceResponse(event_gen())


@router.post("/{mid}/end")
async def end_meeting(mid: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    m = await _get_meeting(mid, user.id, db)
    r = await db.execute(select(Transcript).where(Transcript.meeting_id == mid).order_by(Transcript.ts))
    chunks = [{"speaker": t.speaker, "text": t.text} for t in r.scalars().all()]
    result = await generate_summary(chunks, m.title)
    m.ended_at = datetime.utcnow()
    m.summary = result.get("summary", "")
    m.action_items_json = json.dumps(result.get("action_items", []))
    await db.commit(); await db.refresh(m)
    return {**MeetingOut.model_validate(m).model_dump(), "follow_up_email": result.get("follow_up_email", "")}


@router.get("", response_model=list[MeetingOut])
async def list_meetings(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Meeting).where(Meeting.user_id == user.id).order_by(Meeting.started_at.desc()))
    return [MeetingOut.model_validate(m) for m in r.scalars().all()]


@router.get("/{mid}")
async def get_meeting(mid: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    m = await _get_meeting(mid, user.id, db)
    r_h = await db.execute(select(Hint).where(Hint.meeting_id == mid).order_by(Hint.created_at))
    r_t = await db.execute(select(Transcript).where(Transcript.meeting_id == mid).order_by(Transcript.ts))
    return {
        **MeetingOut.model_validate(m).model_dump(),
        "hints": [HintOut.model_validate(h).model_dump() for h in r_h.scalars()],
        "transcript": [{"speaker": t.speaker, "text": t.text, "ts": t.ts} for t in r_t.scalars()],
    }
