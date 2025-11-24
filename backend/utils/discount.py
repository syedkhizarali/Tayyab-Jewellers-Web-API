# Very simple loyalty: every 3rd completed order -> discount_percent
def calculate_loyalty_discount(order_count: int) -> float:
    if order_count >= 3 and order_count % 3 == 0:
        return 5.0  # 5% special discount on the 3rd, 6th, ...
    return 0.0
