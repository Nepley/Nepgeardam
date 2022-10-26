from fastapi import FastAPI

from .common.mongo import MongoDB
from .common.collection import Collection
from .common.auth import Authorization

from .routers import quotation
from .routers import echo
from .routers import scheduler
from .routers import anniversary
from .routers import misc

app = FastAPI()
app.include_router(quotation.router)
app.include_router(echo.router)
app.include_router(scheduler.router)
app.include_router(anniversary.router)
app.include_router(misc.router)

@app.get("/")
async def root():
    return {"status": "OK","message": "Up"}