import os
from pathlib import Path

import gspread
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def load_google_requests() -> list[dict]:
    load_dotenv(PROJECT_ROOT / ".env")

    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("В .env не указан GOOGLE_SHEET_ID")

    client = gspread.service_account(
        filename=str(PROJECT_ROOT / "credentials.json"),
        scopes=SCOPES,
    )

    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet("Requests")

    # Читаем значения строками, как при загрузке CSV.
    rows = worksheet.get_all_values()

    expected_headers = [
        "id", "object", "description", "urgency", "status"
    ]

    if not rows:
        raise ValueError("Лист Requests пуст")

    headers = [value.strip() for value in rows[0]]

    if headers != expected_headers:
        raise ValueError(
            f"Ожидаются заголовки: {expected_headers}. "
            f"Получены: {headers}"
        )

    requests = []

    for row in rows[1:]:
        if not any(value.strip() for value in row):
            continue

        # Дополняем пустые ячейки в конце строки.
        values = row + [""] * (len(headers) - len(row))

        requests.append({
            header: value.strip()
            for header, value in zip(headers, values)
        })

    return requests

def save_google_results(results: list[dict]):
    load_dotenv(PROJECT_ROOT / ".env")

    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("В .env не указан GOOGLE_SHEET_ID")

    client = gspread.service_account(
        filename=str(PROJECT_ROOT / "credentials.json"),
        scopes=SCOPES,
    )

    spreadsheet = client.open_by_key(sheet_id)

    try:
        worksheet = spreadsheet.worksheet("Results")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title="Results",
            rows=100,
            cols=10,
        )

    headers = [
        "id",
        "object",
        "description",
        "urgency",
        "status",
        "category",
        "priority",
        "summary",
        "errors",
    ]

    values = [headers]

    for request in results:
        values.append([
            str(request.get(field, ""))
            for field in headers
        ])

    # Эта вкладка предназначена только для результатов программы.
    # При каждом запуске её содержимое заменяется.
    worksheet.clear()

    worksheet.resize(
        rows=max(len(values), 100),
        cols=len(headers),
    )

    worksheet.update(
        range_name="A1",
        values=values,
        value_input_option="RAW",
    )

    worksheet.freeze(rows=1)

