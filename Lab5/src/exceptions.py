class DuplicateIdError(Exception):
    """Запись с таким id уже есть в базе."""
    pass


class RecordNotFoundError(Exception):
    """Записи с таким id нет в базе."""
    pass