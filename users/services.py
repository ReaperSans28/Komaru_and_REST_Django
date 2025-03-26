import os

import requests
import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

api_key1 = os.getenv("API_KEY")


def convert_rub_to_dollar(price: int) -> int:
    """
    Выдает актуальный курс рубля по отношению к доллару.
    Принимает значение price в долларах и возвращает эквивалент в рублях.
    """
    global api_key1

    url = "https://open.er-api.com/v6/latest/USD"
    headers = {"apikey": api_key1}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and "rates" in data:
            if "RUB" in data["rates"]:
                usd_to_rub_rate = data["rates"]["RUB"]
                converted_value = int(price * usd_to_rub_rate)
                return converted_value

    except Exception as e:
        print(f"Ошибка при получении курса: {e}")

    print("Курс не найден или возникла ошибка.")
    return 0


def create_stripe_price(amount):
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/success",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
