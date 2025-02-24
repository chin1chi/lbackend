import datetime
import json

from .redis import redis_client


async def store_code(phone: str, code: str):
    await redis_client.set(f"code:{phone}", code, ex=300)  # Код хранится 5 минут


async def get_code(phone: str):
    return await redis_client.get(f"code:{phone}")


async def delete_code(phone: str):
    await redis_client.delete(f"code:{phone}")


########################## NOTIFICATION CACHE ##########################

async def get_notifications_cache(current_user_id: int, is_checked: bool | None):
    return await redis_client.get(f"notifications:{current_user_id}:{is_checked}")


async def set_notifications_cache(current_user_id: int, is_checked: bool | None, notifications: list):
    notifications_list = [{"id": notification.id, "message": notification.message} for notification in notifications]
    await redis_client.set(f"notifications:{current_user_id}:{is_checked}", json.dumps(notifications_list), ex=3)


async def delete_notifications_cache(current_user_id: int, is_checked: bool | None):
    await redis_client.delete(f"notifications:{current_user_id}:{is_checked}")


########################## CATEGORIES CACHE ##########################

async def get_categories_cache(current_user_id: int):
    return await redis_client.get(f"categories:{current_user_id}")


async def set_categories_cache(current_user_id: int, categories: dict):
    await redis_client.set(f"categories:{current_user_id}", json.dumps(categories), ex=3)


async def delete_categories_cache(current_user_id: int):
    await redis_client.delete(f"categories:{current_user_id}")


########################## RATING CACHE ##########################

async def get_rating_cache(current_user_id: int, period: str):
    return await redis_client.get(f"rating:{current_user_id}:{period}")


async def set_rating_cache(current_user_id: int, period: str, rating: list):
    rating_list = [
        {"position": number.position, "username": number.username, "points_value": number.points_value}
        for number in rating
    ]
    await redis_client.set(f"rating:{current_user_id}:{period}", json.dumps(rating_list), ex=3)


async def delete_rating_cache(current_user_id: int, period: str):
    await redis_client.delete(f"rating:{current_user_id}:{period}")


########################## EVENTS CACHE ##########################

################# random_events cache #################
async def get_random_events_cache(current_user_id: int, count_events: int):
    return await redis_client.get(f"random_events:{current_user_id}:{count_events}")


async def set_random_events_cache(current_user_id: int, count_events: int, random_events: list):
    random_events_list = [
        {"id": event.id, "name": event.name, "description": event.description, "media": event.media}
        for event in random_events
    ]
    await redis_client.set(f"random_events:{current_user_id}:{count_events}", json.dumps(random_events_list), ex=3)


async def delete_random_events_cache(current_user_id: int, count_events: int):
    await redis_client.delete(f"random_events:{current_user_id}:{count_events}")


################# swipe_events cache #################
async def get_swipe_events_cache(current_user_id: int, is_like_swipe_events: bool):
    return await redis_client.get(f"swipe_events:{current_user_id}:{is_like_swipe_events}")


async def set_swipe_events_cache(current_user_id: int, is_like_swipe_events: bool, swipe_events: list):
    swipe_events_list = [
        {"id": event.id, "name": event.name, "description": event.description, "media": event.media}
        for event in swipe_events
    ]
    await redis_client.set(f"swipe_events:{current_user_id}:{is_like_swipe_events}", json.dumps(swipe_events_list),
                           ex=3)


async def delete_swipe_events_cache(current_user_id: int, is_like_swipe_events: bool):
    await redis_client.delete(f"swipe_events:{current_user_id}:{is_like_swipe_events}")


################# ongoing_events cache #################
async def get_ongoing_events_cache(current_user_id: int):
    return await redis_client.get(f"ongoing_events:{current_user_id}")


async def set_ongoing_events_cache(current_user_id: int, ongoing_events: list):
    ongoing_events_list = [
        {"name": event.name, "description": event.description, "location": event.location}
        for event in ongoing_events
    ]
    await redis_client.set(f"ongoing_events:{current_user_id}", json.dumps(ongoing_events_list), ex=3)


async def delete_ongoing_events_cache(current_user_id: int):
    await redis_client.delete(f"ongoing_events:{current_user_id}")


################# details_event cache #################
async def get_details_event_cache(event_id: int):
    return await redis_client.get(f"details_event:{event_id}")


async def set_details_event_cache(event_id: int, details_event):
    details_event_dict = {
        "name": details_event.name,
        "description": details_event.description,
        "location": details_event.location,
        "started_at": details_event.started_at.isoformat(),
        "expired_at": details_event.expired_at.isoformat(),
        "price": float(details_event.price),
        "media": details_event.media,
        "inst": details_event.inst}

    await redis_client.set(f"details_event:{event_id}", json.dumps(details_event_dict), ex=5)


async def delete_details_event_cache(event_id: int):
    await redis_client.delete(f"details_event:{event_id}")


################# event_history cache #################
async def get_event_history_cache(current_user_id: int, dtfrom: datetime.date, dtto: datetime.date):
    return await redis_client.get(f"event_history:{current_user_id}:{dtfrom}:{dtto}")


async def set_event_history_cache(current_user_id: int, dtfrom: datetime.date, dtto: datetime.date, event_history):
    events_history_list = [
        {
            "event_name": event.event.name,
            "description": event.event.description,
            "state": event.state,
        }
        for event in event_history
    ]
    await redis_client.set(f"event_history:{current_user_id}:{dtfrom}:{dtto}", json.dumps(events_history_list), ex=5)


async def delete_event_history_cache(current_user_id: int, dtfrom: datetime.date, dtto: datetime.date):
    await redis_client.delete(f"event_history::{current_user_id}:{dtfrom}:{dtto}")
