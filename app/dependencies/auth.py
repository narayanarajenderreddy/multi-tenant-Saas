from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.dependencies.db import get_db
from app.models.user import User

security = HTTPBearer()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token:HTTPAuthorizationCredentials  = Depends(security),
                     db:Session = Depends(get_db)):
    verifiedtoken  = token.credentials
    
    decode_data = decode_access_token(verifiedtoken)
    user_id = decode_data.get("user_id")
    tenant_id = decode_data.get("tenant_id")
    
    if decode_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            message = "Invalid token")
    
    
    user = db.query(User).filter(User.id == user_id,User.tenant_id == tenant_id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            message = "User is not found")
    
    
    return user    
            