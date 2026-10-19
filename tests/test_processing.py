from src.validator import validate_request, is_duplicate
from src.classifier import analyze_request
from src.main import process_requests

def make_request(**changes):
    request = {
        "id": "1",
        "object": "Apartment 24",
        "description": "Не работает кондиционер",
        "urgency": "Высокая",
        "status": "Новая",
    }
    request.update(changes)
    return request

def test_valid_request():
    assert validate_request(make_request()) == []

def test_empty_description():
    request = make_request(description="   ")
    errors = validate_request(request)

    assert "Не заполнено поле: description" in errors

def test_invalid_urgency():
    request = make_request(urgency="Очень высокая")
    errors = validate_request(request)

    assert "Некорректное значение срочности" in errors

def test_duplicate():
    first = make_request(id="1")
    second = make_request(id="2")

    assert is_duplicate(first, [first, second]) is True

def test_request_is_not_its_own_duplicate():
    request = make_request()

    assert is_duplicate(request, [request]) is False

def test_repair_category():
    result = analyze_request(
        "Не работает кондиционер",
        "Высокая",
    )

    assert result["category"] == "Ремонт"
    assert result["priority"] == "Высокий"

def test_cleaning_category():
    result = analyze_request(
        "В квартире грязно и нужны полотенца",
        "Средняя",
    )

    assert result["category"] == "Уборка"
    assert result["priority"] == "Средний"

def test_processing_valid_request():
    results = process_requests([make_request()])

    assert len(results) == 1
    assert results[0]["category"] == "Ремонт"
    assert results[0]["errors"] == ""

def test_processing_invalid_request():
    results = process_requests([
        make_request(description="")
    ])

    assert results[0]["errors"]
    assert "category" not in results[0]


