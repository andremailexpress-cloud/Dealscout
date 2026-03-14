# Deal Hunter Pro X - Safety Analyzer
# All risk language is legally sound: uses "indicators" and "risk factors", not accusations.

import re

RISK_INDICATORS = {
    "price_too_low": {
        "label": "Price significantly below market value",
        "weight": 25,
        "patterns": [],
    },
    "urgency_language": {
        "label": "Urgency indicators present in listing",
        "weight": 15,
        "patterns": [
            r"\burgent\b", r"\bquick sale\b", r"\bgoing fast\b", r"\blast chance\b",
            r"\btoday only\b", r"\bmust go\b", r"\bno time wasters\b", r"\bserious buyers only\b",
            r"\bprice is final\b", r"\bno lowball\b",
        ],
    },
    "payment_upfront": {
        "label": "Advance payment requested prior to inspection",
        "weight": 30,
        "patterns": [
            r"\beft before\b", r"\bpayment upfront\b", r"\bdeposit to reserve\b",
            r"\bsend money\b", r"\bcash upfront\b", r"\bpay first\b",
            r"\bcrypto\b", r"\bbitcoin\b", r"\bpaypal\b",
        ],
    },
    "contact_offsite": {
        "label": "Off-platform communication requested",
        "weight": 20,
        "patterns": [
            r"\bwhatsapp only\b", r"\bcontact via whatsapp\b", r"\btelegram only\b",
            r"\bemail only\b", r"\bno calls\b", r"\btext only\b",
        ],
    },
    "no_meetup": {
        "label": "In-person viewing or meetup declined",
        "weight": 20,
        "patterns": [
            r"\bno meetup\b", r"\bwill ship\b", r"\bship nationwide\b",
            r"\bno pickups\b", r"\bdelivery only\b", r"\bno viewings\b",
        ],
    },
    "new_account": {
        "label": "Indicators of recently created seller profile",
        "weight": 15,
        "patterns": [
            r"\bnew account\b", r"\bnew seller\b", r"\bjust joined\b",
        ],
    },
    "no_returns": {
        "label": "No returns or recourse policy stated",
        "weight": 10,
        "patterns": [
            r"\bno returns\b", r"\bno refund\b", r"\bas is\b", r"\bsold as seen\b",
        ],
    },
    "poor_description": {
        "label": "Limited listing detail or verification information",
        "weight": 10,
        "patterns": [],
    },
}

TRUST_SIGNALS_PATTERNS = {
    "receipt_available": {
        "label": "Proof of purchase or receipt available",
        "patterns": [r"\breceipt\b", r"\binvoice\b", r"\bwarranty\b", r"\bcertificate\b"],
    },
    "public_meetup": {
        "label": "Willingness to meet at public/verifiable location",
        "patterns": [
            r"\bmall\b", r"\bshopping cent\b", r"\babsa\b", r"\bfnb branch\b",
            r"\bpublic place\b", r"\bcafe\b", r"\bpickup from\b",
        ],
    },
    "detailed_description": {
        "label": "Detailed and specific product description provided",
        "patterns": [],
    },
    "original_box": {
        "label": "Original packaging and accessories included",
        "patterns": [r"\boriginal box\b", r"\ball accessories\b", r"\boriginal charger\b"],
    },
    "service_history": {
        "label": "Service history or maintenance records available",
        "patterns": [r"\bservice history\b", r"\bfull service\b", r"\bdealer service\b"],
    },
    "test_drive": {
        "label": "Test drive or inspection welcomed",
        "patterns": [r"\btest drive\b", r"\btest drives welcome\b", r"\binspection\b", r"\bcan view\b"],
    },
    "authenticated_product": {
        "label": "Authentication documentation referenced",
        "patterns": [r"\bauthentic\b", r"\blegit\b", r"\bverified\b", r"\bcertificate of auth\b"],
    },
}

RISK_LEVEL_MAP = {
    (0, 20): ("LOW", "Safe to proceed with standard due diligence."),
    (21, 40): ("CAUTION", "Exercise due diligence — verify item details and seller profile before proceeding."),
    (41, 65): ("ELEVATED RISK", "Multiple risk indicators identified. Recommend in-person inspection and verification before any payment."),
    (66, 100): ("HIGH RISK", "Significant risk indicators detected. Seek independent verification and avoid advance payment arrangements."),
}


def _get_risk_level_and_recommendation(score: int):
    for (low, high), (level, recommendation) in RISK_LEVEL_MAP.items():
        if low <= score <= high:
            return level, recommendation
    return "ELEVATED RISK", "Verify before proceeding."


def analyze_text(text: str) -> dict:
    """
    Analyze listing text for risk indicators.
    Returns a dict with: risk_score, risk_level, indicators_found, trust_signals, recommendation
    """
    if not text or not text.strip():
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "indicators_found": [],
            "trust_signals": ["No text provided for analysis"],
            "recommendation": "Provide listing text for a full assessment.",
        }

    text_lower = text.lower()
    indicators_found = []
    total_weight = 0

    # Check each risk indicator
    for key, indicator in RISK_INDICATORS.items():
        if key == "poor_description":
            # Flag if text is very short
            if len(text.strip()) < 80:
                indicators_found.append(indicator["label"])
                total_weight += indicator["weight"]
            continue

        if indicator["patterns"]:
            for pattern in indicator["patterns"]:
                if re.search(pattern, text_lower):
                    indicators_found.append(indicator["label"])
                    total_weight += indicator["weight"]
                    break  # only count each indicator once

    # Check trust signals
    trust_signals_found = []
    for key, signal in TRUST_SIGNALS_PATTERNS.items():
        if key == "detailed_description":
            if len(text.strip()) > 200:
                trust_signals_found.append(signal["label"])
            continue
        for pattern in signal["patterns"]:
            if re.search(pattern, text_lower):
                trust_signals_found.append(signal["label"])
                break

    # Reduce score for trust signals found
    trust_reduction = len(trust_signals_found) * 5

    # Clamp risk score between 0 and 100
    risk_score = max(0, min(100, total_weight - trust_reduction))

    risk_level, recommendation = _get_risk_level_and_recommendation(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators_found": list(set(indicators_found)),
        "trust_signals": trust_signals_found if trust_signals_found else ["No positive trust signals detected"],
        "recommendation": recommendation,
    }


def analyze_url(url: str) -> dict:
    """
    Analyze a URL for surface-level risk indicators.
    For a live implementation this would fetch and parse the listing.
    Currently returns a structured placeholder result with URL-based checks.
    """
    indicators_found = []
    trust_signals = []
    risk_score = 10

    url_lower = url.lower()

    # Check for known legitimate platforms
    known_safe_platforms = ["facebook.com", "gumtree.co.za", "olx.co.za", "webuycars.co.za", "marketplace"]
    on_known_platform = any(p in url_lower for p in known_safe_platforms)

    if on_known_platform:
        trust_signals.append("Listing hosted on a recognised South African marketplace platform")
        risk_score = max(0, risk_score - 10)
    else:
        indicators_found.append("Listing URL does not match a known South African marketplace platform")
        risk_score += 15

    # Check for suspicious URL patterns
    if any(x in url_lower for x in ["bit.ly", "tinyurl", "t.co", "short.link"]):
        indicators_found.append("Shortened URL detected — destination unverified")
        risk_score += 20

    risk_level, recommendation = _get_risk_level_and_recommendation(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators_found": indicators_found if indicators_found else ["No URL-level risk indicators detected"],
        "trust_signals": trust_signals if trust_signals else ["No URL-based trust signals identified"],
        "recommendation": recommendation
        + " Note: For a full assessment, paste the listing text directly.",
    }
