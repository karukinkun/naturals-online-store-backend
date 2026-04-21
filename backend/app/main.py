from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 全モデルをロード（超重要）
import app.models

# router
from app.routers import products, ratings, users

origins = [
    "http://localhost:3000",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="Natulalis API",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ルーター登録
    app.include_router(products.router)
    app.include_router(ratings.router)
    app.include_router(users.router)

    return app


app = create_app()
