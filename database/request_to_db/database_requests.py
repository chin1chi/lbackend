from sqlalchemy import update, func, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models.events import Event
from database.models.history_events import HistoryEvent
from database.models.notifications import Notification
from database.models.players import Player
from database.models.partner_users import PartnerUser
from database.models.choose_events import ChooseEvent
from database.models.enums import ChooseEventStatus
from fastapi import HTTPException
from datetime import datetime, timezone
from schemas.error_schemas import NotFoundErrorResponse
from database.models.entertainments import Entertainment
from database.models.swipe_events import SwipeEvent
from database.models.users import User
from schemas.error_schemas import NotFoundErrorResponse
from database.models.history_events import HistoryEvent
from schemas.history_events_schemas import HistoryDateFrom, HistoryDateTo
from sqlalchemy.orm import selectinload


async def get_user_by_phone(phone: str, db: AsyncSession) -> User | None:
    """
    Получить пользователя по номеру телефона.
    """
    result = await db.execute(select(User).filter(User.phone_number == phone))

    return result.scalar_one_or_none()


async def create_user(phone: str, db: AsyncSession) -> User:
    """
    Создать нового пользователя с указанным номером телефона.
    """
    user = User(phone_number=phone)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_player_for_user(user: User, db: AsyncSession):
    # Проверяем, есть ли связь с партнёром через таблицу partner_user
    result = await db.execute(select(PartnerUser).filter(PartnerUser.user_id == user.id))
    partner_user = result.scalar_one_or_none()

    if partner_user is None:
        # Если связи с партнёром нет, создаём игрока
        new_player = Player(user_id=user.id)
        db.add(new_player)
        await db.commit()
        await db.refresh(new_player)  # Обновляем новый объект


async def get_ongoing_events(player_id: int, db: AsyncSession) -> list[Event]:
    stmt = (
        select(Event)
        .join(ChooseEvent)
        .where(
            ChooseEvent.state == ChooseEventStatus.ongoing,
            ChooseEvent.player_id == player_id
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_event_by_id(db: AsyncSession, event_id: int):
    stmt = select(Event).filter(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()  # Получаем одно событие или None, если не найдено
    return event


async def get_player(user_id: int, db: AsyncSession):
    result = await db.execute(select(Player).filter(Player.user_id == user_id))
    player = result.scalar_one_or_none()
    if player is None:
        raise HTTPException(status_code=NotFoundErrorResponse.status, detail=NotFoundErrorResponse.status_text)
    return player


async def get_username_by_user_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=NotFoundErrorResponse.status, detail=NotFoundErrorResponse.status_text)
    return user.username


async def get_user_id_by_player_id(player_id: int, db: AsyncSession):
    result = await db.execute(select(Player).filter(Player.id == player_id))
    player = result.scalar_one_or_none()
    if player is None:
        raise HTTPException(status_code=NotFoundErrorResponse.status, detail=NotFoundErrorResponse.status_text)
    return player.user_id


async def get_category(category_id: int, db: AsyncSession):
    result = await db.execute(select(Entertainment).filter(Entertainment.id == category_id))
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=NotFoundErrorResponse.status, detail=NotFoundErrorResponse.status_text)
    return category


async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(Entertainment))
    return result.scalars().all()


async def update_player_entertainment_tags(player: Player, category_id: int, like_category: bool, db: AsyncSession):
    if like_category:
        if category_id not in player.entertainments_tags:
            player.entertainments_tags.append(category_id)
    else:
        if category_id in player.entertainments_tags:
            player.entertainments_tags.remove(category_id)

    await db.execute(
        update(Player).where(Player.id == player.id).values(entertainments_tags=player.entertainments_tags)
    )
    await db.commit()
    await db.refresh(player)


async def get_event_history_by_dates(player_id: int, dtfrom: datetime, dtto: datetime, db: AsyncSession) -> list[HistoryEvent]:
    """
    Получить события из истории (events_history) для игрока за указанный диапазон дат.
    """

    stmt = (
        select(HistoryEvent).options(selectinload(HistoryEvent.event))
        .where(
            (HistoryEvent.player_id == player_id),

            HistoryEvent.created_at >= dtfrom.date(),
            HistoryEvent.created_at <= dtto.date()
        )

    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def players_rating_all(db: AsyncSession):
    result = await db.execute(select(User.username, Player.points_value)
                              .join(Player, User.id == Player.user_id)
                              .order_by(Player.points_value.desc()))

    return result


async def players_rating_current_month(db: AsyncSession):
    current_month = datetime.now().month
    current_year = datetime.now().year

    result = await db.execute(select(User.username, func.sum(Event.accrued_points))
                              .join(Player, User.id == Player.user_id)
                              .join(HistoryEvent, HistoryEvent.player_id == Player.id)
                              .join(Event, Event.id == HistoryEvent.event_id)
                              .filter(extract('month', HistoryEvent.created_at) == current_month,
                                      extract('year', HistoryEvent.created_at) == current_year
                                      ).group_by(User.username).order_by(func.sum(Event.accrued_points).desc()))

    return result


async def players_rating_current_year(db: AsyncSession):
    current_year = datetime.now().year

    result = await db.execute(select(User.username, func.sum(Event.accrued_points))
                              .join(Player, User.id == Player.user_id)
                              .join(HistoryEvent, HistoryEvent.player_id == Player.id)
                              .join(Event, Event.id == HistoryEvent.event_id)
                              .filter(extract('year', HistoryEvent.created_at) == current_year)
                              .group_by(User.username).order_by(func.sum(Event.accrued_points).desc())
                              )
    return result


async def get_number_random_events(user_id, count_events, db: AsyncSession):
    player = await get_player(user_id, db)
    swipe_events = await db.execute(select(SwipeEvent.event_id).filter(SwipeEvent.player_id == player.id))
    swipe_event_ids = swipe_events.scalars().all()

    result = await db.execute(
        select(Event).filter(Event.id.notin_(swipe_event_ids)).order_by(func.random()).limit(count_events))

    events = result.scalars().all()
    return events


async def get_swipe_events(user_id, is_like, db: AsyncSession):
    player = await get_player(user_id, db)

    result = await db.execute(
        select(Event).join(SwipeEvent, SwipeEvent.event_id == Event.id).filter(
            SwipeEvent.player_id == player.id, SwipeEvent.is_like == is_like))

    events = result.scalars().all()
    return events


async def get_swipe_event(user_id: int, event_id: int, db: AsyncSession):
    player = await get_player(user_id, db)
    result = await db.execute(
        select(SwipeEvent).where(SwipeEvent.event_id == event_id, SwipeEvent.player_id == player.id))
    event = result.scalar_one_or_none()
    if event is None:
        return False
    return event


async def add_swipe_event(user_id, event_id, like_event, db: AsyncSession):
    player = await get_player(user_id, db)

    swipe_event = SwipeEvent(event_id=event_id, player_id=player.id, is_like=like_event)

    db.add(swipe_event)
    await db.commit()


async def update_swipe_event(swipe_event, like_event, db: AsyncSession):
    await db.execute(update(SwipeEvent).where(SwipeEvent.id == swipe_event.id).values(is_like=like_event))
    await db.commit()


async def get_notifications(user_id: int, is_checked: bool | None, db: AsyncSession):
    if is_checked is None:
        result = await db.execute(select(Notification).filter(Notification.user_id == user_id))
    else:
        result = await db.execute(
            select(Notification).filter(Notification.user_id == user_id, Notification.is_checked == is_checked))
    notifications = result.scalars().all()

    return notifications


async def set_checked_notification_for_user(user_id: int, notification_id: int, db: AsyncSession):
    await db.execute(
        update(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        .values(is_checked=True))
    await db.commit()
