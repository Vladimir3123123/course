# BankWidget - Анализ банковских транзакций

Приложение для анализа транзакций из Excel-файлов. Генерирует JSON-данные для веб-страниц, предоставляет сервисы поиска и формирует отчеты о расходах.

## 🛠 Стек технологий
* **Python 3.12**
* **pandas** — обработка и анализ табличных данных
* **requests** — интеграция с внешними API (курсы валют ЦБ РФ, акции Yahoo Finance)
* **pytest** — тестирование
* **flake8 / isort** — линтинг и форматирование кода

## 📂 Структура проекта
```text
.
├── data/
│   └── transactions_excel.xlsx  # Исходные данные
├── src/
│   ├── main.py                  # Интерактивное меню
│   ├── views.py                 # Генерация JSON для главной страницы
│   ├── services.py              # Сервисы (поиск)
│   ├── reports.py               # Отчеты (траты по категориям)
│   └── utils.py                 # Вспомогательные функции и работа с API
├── tests/                       # Тесты
├── user_settings.json           # Настройки валют и акций
└── README.md
```

## ⚙️ Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone <ссылка_на_репозиторий>
   cd Coursework
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv .venv
   # Для Windows:
   .venv\Scripts\activate
   # Для Mac/Linux:
   source .venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
   *(Если файла requirements.txt нет, установите вручную: `pip install pandas requests openpyxl pytest`)*

## 🚀 Использование

### 1. Главная страница (генерация JSON)
Модуль `views.py` формирует JSON-ответ с приветствием, статистикой по картам, топ-5 транзакциями, курсами валют и акциями на заданную дату.
```bash
python -m src.views
```

### 2. Интерактивное меню
Модуль `main.py` запускает консольный интерфейс для фильтрации транзакций по статусу и дате.
```bash
python -m src.main
```

### 3. Сервисы и Отчеты
**Простой поиск** по описанию или категории:
```python
from src.utils import get_transactions_data
from src.services import simple_search
import pandas as pd

txs = get_transactions_data("data/transactions_excel.xlsx")
df = pd.DataFrame(txs)
results = simple_search(df, "Перевод")
print(f"Найдено: {len(results)}")
```

**Отчет «Траты по категории»** с сохранением в JSON:
```python
from src.reports import spending_by_category
# Ищет траты в евро за последние 3 месяца от указанной даты
report = spending_by_category(df, "Euro", "10.11.2023")
```

## 🧪 Тестирование
Для запуска тестов используйте:
```bash
python -m pytest tests/ -v
```
Покрытие кода тестами составляет более 80%.

## 📊 Настройки
Файл `user_settings.json` позволяет задать список интересующих валют и акций:
```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```