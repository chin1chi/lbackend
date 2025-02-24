from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_routes import router as auth_router
from events.get_events import router as get_events_router
from events.get_complete_events import router as get_complete_events_router
from notifications.get_notifications import router as get_notifications_router
from categoryes.get_categories import router as categories_router
from rating.get_rating import router as rating_router
from events.get_swipe_events import router as get_swipe_events_router
from middlewares.Token_valid import TokenValidationMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TokenValidationMiddleware)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(get_events_router, prefix="/events", tags=["events"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(get_complete_events_router,prefix="/history_events",tags=["history_events"])
app.include_router(rating_router, prefix="/rating", tags=["rating"])
app.include_router(get_swipe_events_router, prefix="/events", tags=["events"])
app.include_router(get_notifications_router, prefix="/notifications", tags=["notifications"])
