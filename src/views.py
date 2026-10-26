from datetime import datetime

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, get_user_settings


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени."""
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_cards_info(df_month: pd.DataFrame) -> list[dict]:
    """Считает траты и кешбэк по каждой карте."""
    df = df_month[df_month["card_from"].notna()]

    cards = []
    for card, group in df.groupby("card_from"):
        total_spent = abs(group["amount"].sum())
        card_str = str(card).split()[-1]
        last_digits = card_str[-4:] if len(card_str) >= 4 else card_str
        cards.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": round(total_spent / 100, 2)
        })
    return cards


def get_top_transactions(df_month: pd.DataFrame) -> list[dict]:
    """Возвращает топ-5 транзакций по сумме."""
    df = df_month.sort_values(by="amount", ascending=False).head(5)

    top = []
    for _, row in df.iterrows():
        dt = row["date"].strftime("%d.%m.%Y")
        top.append({
            "date": dt,
            "amount": float(row["amount"]),
            "category": "Без категории",
            "description": row.get("description", "")
        })
    return top


def main_view(date_str: str, transactions: list[dict]) -> dict:
    """Главная функция для генерации JSON ответа главной страницы."""
    current_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_of_month = current_dt.replace(day=1, hour=0, minute=0, second=0)

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    df_month = df[(df["date"] >= start_of_month) & (df["date"] <= current_dt)]

    settings = get_user_settings()

    return {
        "greeting": get_greeting(current_dt),
        "cards": get_cards_info(df_month),
        "top_transactions": get_top_transactions(df_month),
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", []))
    }


if __name__ == "__main__":
    from src.utils import get_transactions_data
    import json

    txs = get_transactions_data("data/transactions_excel.xlsx")

    result = main_view("2023-11-10 23:59:59", txs)

    print(json.dumps(result, ensure_ascii=False, indent=4))