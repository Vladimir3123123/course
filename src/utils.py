import json

import pandas as pd
import requests

def get_transactions_data(file_path: str) -> list[dict]:
    """Читает Excel-файл и возвращает список транзакций."""
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"from": "card_from", "to": "card_to"})
    return df.to_dict(orient="records")


def get_user_settings(file_path: str = "user_settings.json") -> dict:
    """Загружает настройки пользователя из JSON."""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def get_currency_rates(currencies: list[str]) -> list[dict]:
    """Получает официальные курсы валют ЦБ РФ (не требует ключей)."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        rates = data.get("Valute", {})

        result = []
        for cur in currencies:
            if cur in rates:
                nominal = rates[cur].get("Nominal", 1)
                value = rates[cur].get("Value", 0)
                rate = value / nominal
                result.append({"currency": cur, "rate": round(rate, 2)})
            else:
                result.append({"currency": cur, "rate": 0.0})
        return result
    except Exception as e:
        print(f"Ошибка ЦБ: {e}")
        return [{"currency": cur, "rate": 90.0} for cur in currencies]


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Получает цены акций через публичный API Yahoo Finance (не требует ключей)."""
    result = []
    for stock in stocks:
        try:
            # Публичный endpoint Yahoo Finance
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            data = response.json()

            # Вытаскиваем текущую цену (regularMarketPrice)
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            result.append({"stock": stock, "price": round(float(price), 2)})
        except Exception:
            # Если не получилось достать, ставим заглушку
            result.append({"stock": stock, "price": 150.0})

    return result