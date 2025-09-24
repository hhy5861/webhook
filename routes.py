from fastapi import APIRouter, Request, HTTPException
import httpx
from config import WECOM_WEBHOOK, TIMEOUT
from services import text_notice_card

router = APIRouter()

@router.post("/hooks/alertmanager")
async def to_wecom_card(request: Request):
    """接收 Alertmanager webhook 并转发到企业微信"""
    if not WECOM_WEBHOOK:
        raise HTTPException(500, "WECOM_WEBHOOK not set")
    
    payload = await request.json()
    alerts = payload.get("alerts", [])
    if not alerts:
        return {"ok": True, "sent": 0}

    # 只示例首条（群机器人卡片一般一条一张，若要合并可自定义"news_notice"类型或发送多张）
    body = text_notice_card(alerts[0])

    async with httpx.AsyncClient(timeout=TIMEOUT) as cli:
        r = await cli.post(WECOM_WEBHOOK, json=body)
        data = {}
        try: 
            data = r.json()
        except Exception: 
            pass
        if r.status_code != 200 or data.get("errcode") != 0:
            raise HTTPException(502, f"WeCom error: {r.text}")
    
    return {"ok": True, "sent": 1}
