# Deal Hunter Pro X - Deal Value Scorer
# Compares deal price against mock market averages to compute a value score (0-100).

MARKET_AVERAGES = {
    # Electronics
    "laptop": 18000,
    "macbook": 28000,
    "iphone": 18000,
    "samsung galaxy": 16000,
    "ipad": 16000,
    "tv": 15000,
    "oled": 20000,
    "qled": 18000,
    "camera": 20000,
    "canon": 20000,
    "tablet": 10000,
    # Vehicles
    "fortuner": 580000,
    "ranger": 520000,
    "polo": 210000,
    "bakkie": 400000,
    "motorbike": 75000,
    "honda cb": 80000,
    # Furniture
    "lounge suite": 28000,
    "couch": 12000,
    "bed": 15000,
    "office chair": 20000,
    "herman miller": 26000,
    "desk": 8000,
    # Tools
    "dewalt": 4500,
    "makita": 8000,
    "bosch tools": 5000,
    "drill": 2500,
    # Gaming
    "ps5": 10000,
    "xbox series": 9500,
    "ps4 pro": 5500,
    "nintendo switch": 5000,
    # Appliances
    "fridge": 14000,
    "washing machine": 9000,
    "dyson": 12000,
    "smeg": 22000,
    # Sports & Outdoors
    "mountain bike": 15000,
    "trek": 16000,
    "golf clubs": 10000,
    # Clothing & Shoes
    "jordan": 4000,
    "nike": 3500,
    "adidas": 2500,
    # Books
    "harry potter": 5000,
    # Collectibles
    "krugerrand": 44000,
}

DEFAULT_CATEGORY_AVERAGES = {
    "Electronics": 15000,
    "Vehicles": 350000,
    "Furniture": 12000,
    "Tools": 5000,
    "Clothing": 2000,
    "Sports": 8000,
    "Gaming": 8000,
    "Appliances": 9000,
    "Books": 500,
    "Collectibles": 15000,
}


def _find_market_average(title: str, category: str) -> float:
    """Find the closest market average for a given title."""
    title_lower = title.lower()
    for keyword, avg in MARKET_AVERAGES.items():
        if keyword in title_lower:
            return avg
    return DEFAULT_CATEGORY_AVERAGES.get(category, 10000)


def score_deal(title: str, price: float, category: str, original_price: float = None) -> dict:
    """
    Score a deal based on how good the price is vs market average.
    Returns: value_score (0-100), saving_amount, saving_pct, market_avg
    """
    market_avg = _find_market_average(title, category)

    if original_price and original_price > price:
        # Use original_price as reference if available and higher than price
        reference = original_price
    else:
        reference = market_avg

    if reference <= 0:
        return {"value_score": 50, "saving_amount": 0, "saving_pct": 0, "market_avg": market_avg}

    saving_pct = ((reference - price) / reference) * 100
    saving_amount = reference - price

    # Score: 0% saving = 0 score, 70%+ saving = 100 score (linear with cap)
    raw_score = min(100, max(0, (saving_pct / 70) * 100))
    value_score = int(raw_score)

    return {
        "value_score": value_score,
        "saving_amount": round(saving_amount, 2),
        "saving_pct": round(saving_pct, 1),
        "market_avg": market_avg,
    }


def get_value_label(score: int) -> str:
    """Return a human-readable label for a value score."""
    if score >= 85:
        return "Exceptional Value"
    elif score >= 70:
        return "Great Deal"
    elif score >= 55:
        return "Good Value"
    elif score >= 40:
        return "Fair Price"
    elif score >= 25:
        return "Below Average Saving"
    else:
        return "Near Market Price"


def get_score_color(score: int) -> str:
    """Return a hex color for a given value score."""
    if score >= 80:
        return "#22c55e"  # green
    elif score >= 60:
        return "#f59e0b"  # amber
    elif score >= 40:
        return "#f97316"  # orange
    else:
        return "#ef4444"  # red
