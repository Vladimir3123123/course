import pandas as pd


def simple_search(df: pd.DataFrame, query: str) -> list[dict]:
    """Ищет транзакции по подстроке в описании или валюте."""
    if not query:
        return []

    query_lower = query.lower()
    result = []

    for _, row in df.iterrows():
        desc = str(row.get("description", "")).lower()
        cat = str(row.get("currency_name", "")).lower()

        if query_lower in desc or query_lower in cat:
            row_dict = row.to_dict()
            if pd.notna(row_dict.get("date")):
                row_dict["date"] = row_dict["date"].strftime("%d.%m.%Y")
            result.append(row_dict)

    return result