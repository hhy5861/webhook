from fastapi import APIRouter, Request, HTTPException
import httpx
import logging
from config import WECOM_WEBHOOK, TIMEOUT
from services import text_notice_card

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/hooks/alertmanager")
async def to_wecom_card(request: Request):
    """接收 Alertmanager webhook 并转发到企业微信"""
    try:
        if not WECOM_WEBHOOK:
            logger.error("WECOM_WEBHOOK environment variable not set")
            raise HTTPException(500, "WECOM_WEBHOOK not set")
        
        logger.info(f"WECOM_WEBHOOK configured: {WECOM_WEBHOOK[:20]}...")
        
        payload = await request.json()
        logger.info(f"Received payload with {len(payload.get('alerts', []))} alerts")
        
        alerts = payload.get("alerts", [])
        if not alerts:
            logger.info("No alerts in payload, returning success")
            return {"ok": True, "sent": 0}

        # 只示例首条（群机器人卡片一般一条一张，若要合并可自定义"news_notice"类型或发送多张）
        logger.info("Generating WeCom card for first alert")
        body = text_notice_card(alerts[0])
        logger.info(f"Generated card body: {body}")

        logger.info(f"Sending request to WeCom webhook with timeout {TIMEOUT}s")
        async with httpx.AsyncClient(timeout=TIMEOUT) as cli:
            r = await cli.post(WECOM_WEBHOOK, json=body)
            logger.info(f"WeCom response status: {r.status_code}")
            logger.info(f"WeCom response text: {r.text}")
            
            data = {}
            try: 
                data = r.json()
                logger.info(f"WeCom response data: {data}")
            except Exception as e: 
                logger.warning(f"Failed to parse WeCom response as JSON: {e}")
                pass
                
            if r.status_code != 200 or data.get("errcode") != 0:
                logger.error(f"WeCom API error: status={r.status_code}, errcode={data.get('errcode')}, text={r.text}")
                raise HTTPException(502, f"WeCom error: {r.text}")
        
        logger.info("Successfully sent alert to WeCom")
        return {"ok": True, "sent": 1}
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in to_wecom_card: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Internal server error: {str(e)}")
