from fastapi import FastAPI
from app.api import router
from app.db import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
