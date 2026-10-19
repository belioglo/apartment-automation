
def analyze_request(description: str, urgency: str) -> dict:
    text = description.lower()

    if any(word in text for word in [
        "кондиционер", "лампочка", "протечка", "кран", "ремонт"
    ]):
        category = "Ремонт"
    elif any(word in text for word in [
        "грязно", "уборка", "полотенца"
    ]):
        category = "Уборка"
    elif any(word in text for word in [
        "бронирование", "заселение", "выселение"
    ]):
        category = "Бронирование"
    else:
        category = "Другое"

    priority = {
        "Высокая": "Высокий",
        "Средняя": "Средний",
        "Низкая": "Низкий"
    }.get(urgency, "Средний")

    return {
        "category": category,
        "priority": priority,
        "summary": f"Заявка относится к категории «{category}»."
    }

