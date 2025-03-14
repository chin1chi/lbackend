import json
import qrcode
import os
from fastapi import APIRouter, Request,Depends, HTTPException
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_player
from  middlewares.Token_valid import get_current_user_id
from schemas.error_schemas import InternalServerErrorResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import history_events

router = APIRouter()

QR_CODE_DIR = "static/qrcodes"
os.makedirs(QR_CODE_DIR, exist_ok=True)

async def check_if_event_completed(user_id:int, event_id:int,db:AsyncSession)->bool:
    result=await db.execute(
        select(history_events).filter_by(user_id=user_id,event_id=event_id,state="completed")
    )
    event=result.scalar().first()
    
    return event is not None

@router.post("/generate_qr")
async def generate_qr(
    event_id: int,
    request: Request,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)

):
    # Получаем player_id по user_id
    player = await get_player(user_id, db)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    data = {"player_id": player.id, "event_id": event_id}
    qr = qrcode.make(json.dumps(data))
    qr_filename = f"qr_{player.id}_{event_id}.png"
    qr_path = os.path.join(QR_CODE_DIR, f"qr_{player.id}_{event_id}.png")
    qr.save(qr_path)

    qr_url = str(request.base_url) + f"static/qrcodes/{qr_filename}"
    return {"qr_url": qr_url}

