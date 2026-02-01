class ObjectCreateError(Exception):
    """Вызывается при ошибке создания объекта URLMap."""
    pass


class ShortGenerateError(Exception):
    """Вызывается, если не удалось сгенерировать уникальный короткий ID."""
    pass
