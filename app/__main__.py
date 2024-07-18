import uvicorn

from fastapi import FastAPI
from api.v1.user_routers import router as user_router
from api.v1.jwt_routers import router as jwt_router
from api.v1.posts_routers import router as post_router

app = FastAPI()
app.include_router(router=user_router, prefix='/user', tags=['user'])
app.include_router(router=jwt_router)
app.include_router(router=post_router,prefix='/posts', tags=['posts'])


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", port=5000, reload=False)   

    