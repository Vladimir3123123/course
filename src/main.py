import pandas as pd

from src.utils import get_transactions_data
from src.services import simple_search
from src.views import get_greeting


def print_transactions(transactions: list[dict]) -> None:
    """Выводит список транзакций в консоль."""
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for tx in transactions:
        date = tx.get("date")
        if hasattr(date, "strftime"):
            date = date.strftime("%d.%m.%Y")

        print(f"{date} {tx.get('description', '')}")

        card_from = tx.get("card_from")
        card_to = tx.get("card_to")
        if pd.notna(card_from):
            print(f"{card_from} -> {card_to}")

        print(f"Сумма: {tx.get('amount')} {tx.get('currency_name')}\n")


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    print("Загружаю данные из Excel-файла...")
    try:
        txs = get_transactions_data("data/transactions_excel.xlsx")
    except FileNotFoundError:
        print("Ошибка: файл data/transactions_excel.xlsx не найден.")
        return

    if not txs:
        print("Файл пуст или не содержит данных.")
        return

    df = pd.DataFrame(txs)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("Ваш выбор: ").strip().upper()
        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен. Попробуйте снова.')

    df_filtered = df[df["state"] == status]
    print(f'Операции отфильтрованы по статусу "{status}"')

    sort_choice = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice in ("да", "yes", "y", "д"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = True if "убыв" in order else False
        df_filtered = df_filtered.sort_values(by="date", ascending=not reverse)

    print("\nРаспечатываю итоговый список транзакций...\n")

    if df_filtered.empty:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        result_txs = df_filtered.to_dict(orient="records")
        print_transactions(result_txs)


if __name__ == "__main__":
    main()