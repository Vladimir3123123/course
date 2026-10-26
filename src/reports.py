import functools
import json
from datetime import datetime
from typing import Callable, Optional

import pandas as pd


def save_report(filename: str = "report.json"):
    """Декоратор для сохранения результата отчёта в файл."""

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if isinstance(result, pd.DataFrame):
                data_to_save = result.to_dict(orient="records")
            else:
                data_to_save = result

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4, default=str)

            return result

        return wrapper

    return decorator


@save_report("spending_by_category.json")
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает траты по категории за последние 3 месяца."""
    if date is None:
        target_date = datetime.now()
    else:
        target_date = datetime.strptime(date, "%d.%m.%Y")

    three_months_ago = target_date - pd.DateOffset(months=3)

    df = transactions.copy()

    # В твоем файле колонки на английском
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    # Фильтрация по датам и категории
    mask = (
            (df["date"] >= three_months_ago) &
            (df["date"] <= target_date) &
            (df["currency_name"] == category)  # Ищем по названию валюты, т.к. Категории нет
    )

    return df[mask]