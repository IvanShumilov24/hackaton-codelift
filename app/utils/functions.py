from uuid import UUID


def _is_valid_uuid(uuid_str: str) -> bool:
    """Проверяет, является ли строка валидным UUID"""
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False
