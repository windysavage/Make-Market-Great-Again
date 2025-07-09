from datetime import datetime, timedelta, timezone


def ensure_datetime_type(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError as e:
            raise ValueError(f'Invalid datetime string format: {value}') from e
    else:
        raise TypeError(f'Expected str or datetime, got {type(value).__name__}')

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))

    return dt
