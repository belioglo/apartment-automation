REQUIRED_FIELDS = ["object", "description", "urgency"]

VALID_URGENCY = {"Низкая", "Средняя", "Высокая"}

def validate_request(request: dict) -> list[str]:
    """
    Проверяет одну заявку и возвращает список ошибок.
    Если ошибок нет, возвращается пустой список.
    """

    errors = []

    for field in REQUIRED_FIELDS:
        value = request.get(field, "")

        if not str(value).strip():
            errors.append(f"Не заполнено поле: {field}")

    if request.get("urgency") not in VALID_URGENCY:
        errors.append("Некорректное значение срочности")

    return errors

def is_duplicate(request: dict, requests: list[dict]) -> bool:
    """
    Проверяет, есть ли среди заявок другая
    с таким же объектом и описанием.
    """

    for item in requests:
        same_object = item.get("object") == request.get("object")
        same_description = (
            item.get("description") == request.get("description")
        )
        another_request = item.get("id") != request.get("id")

        if same_object and same_description and another_request:
            return True

    return False


