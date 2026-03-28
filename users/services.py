import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str, description: str = None) -> str:
    """
    Создаёт продукт в Stripe.
    Возвращает ID созданного продукта.
    """
    product_params = {
        "name": name,
    }
    if description:
        product_params["description"] = description

    try:
        product = stripe.Product.create(**product_params)
        return product.id
    except stripe.error.StripeError as e:

        print(f"Stripe API error (create_product): {e}")
        raise


def create_stripe_price(
    amount_rub: float, product_id: str, currency: str = "rub"
) -> str:
    """
    Создаёт цену для продукта в Stripe.
    amount_rub - сумма в рублях (будет автоматически переведена в копейки).
    Возвращает ID созданной цены.
    """
    try:
        price = stripe.Price.create(
            unit_amount=int(amount_rub * 100),
            currency=currency,
            product=product_id,
        )
        return price.id
    except stripe.error.StripeError as e:
        print(f"Stripe API error (create_price): {e}")
        raise


def create_checkout_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """
    Создаёт сессию Checkout в Stripe.
    Возвращает объект сессии, из которого нужно взять URL.
    """
    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session
    except stripe.error.StripeError as e:
        print(f"Stripe API error (create_session): {e}")
        raise


def create_payment_session(payment, success_url: str, cancel_url: str) -> str:
    """
    Главная функция: по Payment создаёт продукт, цену и сессию в Stripe.
    Возвращает ссылку на оплату (checkout_url).
    """

    if payment.paid_course:
        product_name = payment.paid_course.name
        product_description = payment.paid_course.description
    elif payment.paid_lesson:
        product_name = payment.paid_lesson.name
        product_description = payment.paid_lesson.description
    else:
        raise ValueError("Платёж должен быть связан с курсом или уроком")

    product_id = create_stripe_product(product_name, product_description)

    price_id = create_stripe_price(float(payment.amount), product_id)

    session = create_checkout_session(price_id, success_url, cancel_url)

    return session.url
