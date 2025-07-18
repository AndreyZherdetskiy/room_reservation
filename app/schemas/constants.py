"""
Константы для схем Pydantic (валидация, сообщения, параметры времени).

- MAX_NAME_LENGTH задаёт максимальную длину имени для всех сущностей, где это применимо.
- MIN_NAME_LENGTH задаёт минимальную длину имени для всех сущностей, где это применимо.
- Сообщения и параметры сгруппированы по классам.
- Используется наследование для единых ограничений между слоями (schemas/models).
"""

class SchemaBaseConstants:
    """
    Базовые константы для схем Pydantic.
    MAX_NAME_LENGTH — максимальная длина имени для всех сущностей.
    MIN_NAME_LENGTH — минимальная длина имени для всех сущностей.
    """
    MAX_NAME_LENGTH: int = 100
    MIN_NAME_LENGTH: int = 1

class MeetingRoomMessages:
    """
    Сообщения об ошибках для валидации переговорных комнат.
    """
    EMPTY_NAME: str = 'Строка не должна быть пустой'
    EMPTY_NAME_UPDATE: str = 'Имя переговорки не может быть пустым!'
    NAME_TOO_LONG: str = f'Длина поля не должна превышать {SchemaBaseConstants.MAX_NAME_LENGTH} символов'

class ReservationMessages:
    """
    Сообщения об ошибках для валидации бронирований.
    """
    FROM_LESS_THAN_NOW: str = 'Время начала бронирования не может быть меньше текущего времени'
    FROM_MORE_THAN_TO: str = 'Время начала бронирования не может быть больше времени окончания'

class ReservationTimeDefaults:
    """
    Значения по умолчанию для примеров времени бронирования.
    FROM_MINUTES_SHIFT — смещение старта (минуты).
    TO_HOURS_SHIFT — смещение окончания (часы).
    """
    FROM_MINUTES_SHIFT: int = 10
    TO_HOURS_SHIFT: int = 1 