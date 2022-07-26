from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import models, oauth2
from .. import cr, utils

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cr.execute(
        """ SELECT * FROM users WHERE username =%s""", (user_credentials.username,)
    )
    user = cr.fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = models.User(**user)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.gen_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
