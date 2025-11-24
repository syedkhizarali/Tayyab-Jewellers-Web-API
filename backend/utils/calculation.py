from app.configs import settings

def price_per_gram_from_tola(price_per_tola: float) -> float:
    return price_per_tola / settings.TOla_WEIGHT_GRAM

def karat_price_from_24k_tola(price_per_tola_24k: float, karat: int) -> float:
    return (price_per_tola_24k / 24) * karat
