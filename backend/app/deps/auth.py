import json
from functools import lru_cache
from typing import Any
from urllib.request import urlopen

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

# あなたの環境に合わせて .env から読む形にしてもOKです
COGNITO_REGION = "ap-northeast-3"
COGNITO_USER_POOL_ID = "ap-northeast-3_qfFf7QgF2"
COGNITO_CLIENT_ID = "3lbfdai9j7v4t9gf10qpqsoar2"

COGNITO_ISSUER = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
)

security = HTTPBearer()


class CognitoUser(BaseModel):
    sub: str
    email: str | None = None


@lru_cache
def get_cognito_jwks() -> dict[str, Any]:
    jwks_url = f"{COGNITO_ISSUER}/.well-known/jwks.json"

    with urlopen(jwks_url) as response:
        return json.loads(response.read())


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CognitoUser:
    token = credentials.credentials

    try:
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")

        jwks = get_cognito_jwks()
        key = next((key for key in jwks["keys"] if key["kid"] == kid), None)

        if key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証キーが見つかりません",
            )

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,
            issuer=COGNITO_ISSUER,
        )

        if payload.get("token_use") != "id":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="IDトークンではありません",
            )

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="subが取得できません",
            )

        return CognitoUser(
            sub=sub,
            email=payload.get("email"),
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証トークンが不正です",
        )
