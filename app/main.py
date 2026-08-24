from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.db.database import Base, engine

from app.models.user import User
from app.models.campaigns import Campaign, CampaignMember, CampaignTask

from app.routers import users
from app.routers import campaign
from app.routers import campaign_task
from app.routers import auth


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(campaign.router)
app.include_router(campaign_task.router)
app.include_router(auth.router)


@app.get("/")
def test():
    return {
        "message": "Server đang hoạt động"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )