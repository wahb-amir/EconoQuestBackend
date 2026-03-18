import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "")

def verify_internal_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> bool:
    if not INTERNAL_TOKEN:
        raise RuntimeError("INTERNAL_TOKEN env var not set")
    if credentials.credentials != INTERNAL_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True