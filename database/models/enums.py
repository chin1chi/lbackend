import enum


class TypeValue(enum.Enum):
    """
        int
        bool
        text
        double
    """

    INT = 1
    BOOL = 2
    TEXT = 3
    DOUBLE = 4


class HistoryEventStatus(str, enum.Enum):
    """
        str
    """

    complete = "Завершено"
    cancel = "Отменено"
    timeout = "Истекло время выполнения"


class ChooseEventStatus(str, enum.Enum):
    """
        str
    """
    ongoing = "В процессе"
    complete = "Завершено"
    cancelled = "Отменено"
    pending = "В ожидании"
    failed = "Не удалось"
    timeout = "Истекло время"
