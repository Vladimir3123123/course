import json
from src.utils import get_transactions_data
from src.services import simple_search
from src.reports import spending_by_category
import pandas as pd

txs = get_transactions_data("data/transactions_excel.xlsx")
df = pd.DataFrame(txs)
df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

# 1. Тестируем поиск
print("--- ПОИСК ---")
search_res = simple_search(df, "карту")
print(f"Найдено: {len(search_res)} транзакций")

# 2. Тестируем отчет
print("\n--- ОТЧЕТ ---")
report_res = spending_by_category(df, "Euro", "10.11.2023")
print(f"Трат по категории 'Euro' за 3 месяца: {len(report_res)}")
print("Отчет сохранен в spending_by_category.json")