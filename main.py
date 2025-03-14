from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_routes import router as auth_router
from events.get_events import router as get_events_router
from events.get_complete_events import router as get_complete_events_router
from notifications.get_notifications import router as get_notifications_router
from categoryes.get_categories import router as categories_router
from rating.get_rating import router as rating_router
from events.get_swipe_events import router as get_swipe_events_router
from middlewares.Token_valid import TokenValidationMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer
from events.end_event import router as end_events_router

security = HTTPBearer()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app.get("/secure-data")
async def secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "Secure data", "token": token}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TokenValidationMiddleware)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(get_events_router, prefix="/events", tags=["events"],dependencies=[Depends(security)])
app.include_router(categories_router, prefix="/categories", tags=["categories"],dependencies=[Depends(security)])
app.include_router(get_complete_events_router,prefix="/history_events",tags=["history_events"],dependencies=[Depends(security)])
app.include_router(rating_router, prefix="/rating", tags=["rating"],dependencies=[Depends(security)])
app.include_router(get_swipe_events_router, prefix="/events", tags=["events"],dependencies=[Depends(security)])
app.include_router(get_notifications_router, prefix="/notifications", tags=["notifications"],dependencies=[Depends(security)])

app.include_router(end_events_router, prefix="/events", tags=["end_events"],dependencies=[Depends(security)])

