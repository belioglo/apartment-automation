

from src.google_sheets import (
    load_google_requests,
    save_google_results,
)
import csv
import json
from src.report import create_report
from src.validator import validate_request, is_duplicate
from src.classifier import analyze_request

def load_requests(filename: str) -> list[dict]:
    with open(filename, encoding="utf-8") as file:
        return list(csv.DictReader(file))

def process_requests(requests: list[dict]) -> list[dict]:
    results = []

    for request in requests:
        errors = validate_request(request)

        if is_duplicate(request, requests):
            errors.append("Возможный дубликат")

        if errors:
            request["errors"] = "; ".join(errors)
            results.append(request)
            continue

        analysis = analyze_request(
            request["description"],
            request["urgency"]
        )

        request.update(analysis)
        request["errors"] = ""
        results.append(request)

    return results

def save_results(results: list[dict], filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

def main():
    requests = load_google_requests()

    results = process_requests(requests)

    save_results(
        results,
        "data/processed_requests.json"
    )


    report = create_report(results)

    with open(
        "data/report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print(f"Всего заявок: {report['total_requests']}")
    print(f"Классифицировано: {report['classified_requests']}")
    print(f"Требуют проверки: {report['needs_review']}")
    print("Результаты: data/processed_requests.json")
    print("Сводный отчёт: data/report.json")

    save_google_results(results)
    print("Результаты записаны на вкладку Results")


if __name__ == "__main__":
    main()

