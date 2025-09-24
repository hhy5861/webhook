from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import json
import logging

logger = logging.getLogger(__name__)

class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Capture payload for POST requests to alertmanager webhook
        payload_info = ""
        if request.method == "POST" and request.url.path == "/hooks/alertmanager":
            try:
                # Read the request body
                body = await request.body()
                if body:
                    payload_data = json.loads(body.decode())
                    # Log key information from the payload
                    alerts_count = len(payload_data.get("alerts", []))
                    payload_info = f" - Payload: {alerts_count} alerts"
                    
                    # Log detailed payload for debugging
                    logger.info(f"Alertmanager payload: {json.dumps(payload_data, ensure_ascii=False, indent=2)}")
            except Exception as e:
                payload_info = f" - Payload: Error reading ({str(e)})"
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log access information
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Client: {client_ip} - "
            f"Time: {process_time:.3f}s{payload_info}"
        )
        
        return response
