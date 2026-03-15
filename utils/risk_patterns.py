"""
Deal Hunter Pro X — Risk Pattern Library
South African marketplace-specific pattern matching for listing risk assessment.

All patterns are used solely for automated informational analysis.
Pattern matches indicate statistical risk indicators only and do not constitute
accusations, legal determinations, or definitive claims about any listing or seller.

Sources informed by:
- South African Consumer Protection Act No. 68 of 2008
- National Consumer Commission (NCC) guidelines
- Consumer Goods and Services Ombud (CGSO) best practices
- POPIA (Protection of Personal Information Act) compliance requirements
"""

import re
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# South African specific risk patterns
# ---------------------------------------------------------------------------

SA_RISK_PATTERNS: Dict[str, List[str]] = {
    # Urgency and pressure language commonly associated with elevated-risk listings
    "urgency_phrases": [
        r"\bleaving (the )?country\b",
        r"\bemigratin(g|ated?)\b",
        r"\bselling urgently\b",
        r"\burgent sale\b",
        r"\bneed cash (asap|fast|now|urgently)\b",
        r"\bmust go today\b",
        r"\bmust sell (today|now|asap)\b",
        r"\bprice (is )?negotiable (only )?via whatsapp\b",
        r"\bserious buyers only\b",
        r"\bno time wasters?\b",
        r"\bcollection only,? no viewing\b",
        r"\bno viewing\b",
        r"\bfire sale\b",
        r"\bquick sale\b",
        r"\bsell before (i )?move\b",
        r"\bowner relocating\b",
        r"\bdivorce sale\b",
        r"\bestate sale\b",
        r"\bdownsizing urgently\b",
    ],

    # Payment method patterns associated with elevated transaction risk
    "payment_red_flags": [
        r"\beft before (collection|delivery|viewing)\b",
        r"\bdeposit required\b",
        r"\bdeposit (to )?hold\b",
        r"\bcash on delivery only outside (sa|south africa)\b",
        r"\bbank transfer first\b",
        r"\bsend (the )?money first\b",
        r"\bwestern union\b",
        r"\bmoneygram\b",
        r"\bcash app\b",
        r"\bcrypto(currency)? only\b",
        r"\bbitcoin only\b",
        r"\bskrill\b",
        r"\bbidpay\b",
        r"\bewallet (only|first|before)\b",
        r"\bpaypal (only|first)\b",
        r"\bpayment upfront\b",
        r"\bfull payment (in )?advance\b",
        r"\bpay (before|first|upfront)\b",
        r"\bno refunds\b",
        r"\bno returns?\b",
    ],

    # Off-platform contact patterns (moving communication outside the marketplace)
    "offsite_patterns": [
        r"\bwhatsapp me\b",
        r"\bcontact me on (whatsapp|watsapp|wa)\b",
        r"\bemail only\b",
        r"\bsms me\b",
        r"\bcall me outside (the )?(platform|app|site|gumtree|marketplace)\b",
        r"\bmy (number|cell|phone) is\b",
        r"\+27\s*[67][0-9]{8}",          # SA mobile numbers in listings (context-dependent)
        r"\b0[67][0-9]{8}\b",             # SA local mobile format
        r"\bdo not (use|message) (the )?(platform|chat|inbox)\b",
        r"\bcontact (via|on|through) email\b",
        r"\breply to (my )?email\b",
        r"\bdm me\b",
        r"\binbox me\b",
    ],

    # Suspiciously positive condition claims without substantiation
    "too_good_to_be_true_phrases": [
        r"\bas new\b",
        r"\bnever used\b",
        r"\bsealed (box|in box)\b",
        r"\bfactory (sealed|new)\b",
        r"\bwon (in|at|a) competition\b",
        r"\breceived as (a )?gift\b",
        r"\bbrand new (condition|item|product)\b",
        r"\bmint condition\b",
        r"\bperfect condition\b",
        r"\b100% (genuine|authentic|original|working)\b",
        r"\bguaranteed (genuine|authentic|original|real)\b",
    ],

    # Vehicle-specific elevated risk indicators
    "vehicle_specific": [
        r"\bno (registration )?papers?\b",
        r"\bpapers? (to )?follow\b",
        r"\bpapers? (are )?coming\b",
        r"\bselling on behalf\b",
        r"\bowner (is )?overseas\b",
        r"\bagent (sale|selling)\b",
        r"\bno (vin|chassis|engine) number\b",
        r"\bvin (to )?follow\b",
        r"\bno (roadworthy|roadworthy certificate|rwc)\b",
        r"\bno service history\b",
        r"\baccident (vehicle|damaged|write-off)\b",
        r"\brebuild(ing)? title\b",
        r"\bwritten off\b",
        r"\bsalvage\b",
    ],

    # Electronics-specific elevated risk indicators
    "electronics_specific": [
        r"\bno (serial|imei) number\b",
        r"\bimei (to )?follow\b",
        r"\bicloud (locked|activation lock)\b",
        r"\bfinance (not cleared|outstanding)\b",
        r"\bblacklisted\b",
        r"\bno (original )?charger\b",
        r"\bno (original )?box\b",
        r"\bcracked (screen|display|lcd)\b",
        r"\bwater (damaged|damage)\b",
        r"\bfor (parts|spares) only\b",
        r"\bnot (fully )?functional\b",
    ],

    # Property and rental specific elevated risk indicators
    "property_specific": [
        r"\bowner (is )?overseas\b",
        r"\bcannot (meet|view|show) (in person|personally)\b",
        r"\bkeys? (will be )?sent\b",
        r"\bdeposit (before|to) view(ing)?\b",
        r"\bno viewing (before|until) deposit\b",
        r"\bescrow (service|payment)\b",
        r"\bmanaged (overseas|from abroad)\b",
        r"\bcontact (agent|manager) only\b",
    ],

    # Counterfeit goods indicators
    "authenticity_concerns": [
        r"\breplica\b",
        r"\bcopy\b",
        r"\bA-?grade\b",
        r"\bAAA\b",
        r"\bhigh (quality )?replica\b",
        r"\b1:1 (copy|replica)\b",
        r"\bsame (as|quality as) (original|genuine)\b",
        r"\blooks? (like|exactly like) (the )?(real|original|genuine)\b",
    ],
}


# ---------------------------------------------------------------------------
# Trust-building signals that reduce assessed risk
# ---------------------------------------------------------------------------

LEGITIMATE_TRUST_PATTERNS: Dict[str, List[str]] = {
    "positive_seller_signals": [
        r"\bwill (provide|give|issue) (an? )?(invoice|receipt|slip)\b",
        r"\breceipt (is )?available\b",
        r"\boriginal (packaging|box|receipt|invoice|documentation)\b",
        r"\bcan meet at (a )?(police station|cop shop|saps|mall|public place)\b",
        r"\bviewing (is )?welcome\b",
        r"\btest drive (available|welcome|possible)\b",
        r"\broadworthy certificate (available|included|provided)\b",
        r"\bservice history (available|included|provided)\b",
        r"\bcan (provide|send|show) proof\b",
        r"\brecords? (available|included)\b",
        r"\bfull (service )?history\b",
        r"\bstill under (warranty|guarantee)\b",
        r"\bwarranty (available|included|remaining|transferable)\b",
        r"\bverified (seller|account|profile)\b",
        r"\bid verified\b",
        r"\bcan (view|inspect|see) (in person|personally)\b",
        r"\bin-person (viewing|inspection|collection)\b",
    ],

    "transparent_pricing_signals": [
        r"\bno (hidden )?fees?\b",
        r"\bprice (is )?fixed\b",
        r"\bfirm price\b",
        r"\ball-in price\b",
        r"\bincludes? (vat|delivery|all costs)\b",
    ],

    "legitimate_payment_signals": [
        r"\bcash (on collection|on pickup|preferred)\b",
        r"\bsafe (payment|transaction)\b",
        r"\bpayment (on|at) collection\b",
        r"\bno (deposit|advance payment) (required|needed)\b",
    ],
}


# ---------------------------------------------------------------------------
# Risk weight configuration per pattern category
# ---------------------------------------------------------------------------

PATTERN_RISK_WEIGHTS: Dict[str, int] = {
    "urgency_phrases": 10,
    "payment_red_flags": 25,
    "offsite_patterns": 15,
    "too_good_to_be_true_phrases": 10,
    "vehicle_specific": 20,
    "electronics_specific": 15,
    "property_specific": 20,
    "authenticity_concerns": 30,
}

TRUST_SIGNAL_REDUCTIONS: Dict[str, int] = {
    "positive_seller_signals": 10,
    "transparent_pricing_signals": 5,
    "legitimate_payment_signals": 5,
}


# ---------------------------------------------------------------------------
# Category-to-pattern mapping (which risk pattern sets apply per listing type)
# ---------------------------------------------------------------------------

CATEGORY_PATTERN_SETS: Dict[str, List[str]] = {
    "vehicle": [
        "urgency_phrases",
        "payment_red_flags",
        "offsite_patterns",
        "vehicle_specific",
        "too_good_to_be_true_phrases",
    ],
    "electronics": [
        "urgency_phrases",
        "payment_red_flags",
        "offsite_patterns",
        "electronics_specific",
        "too_good_to_be_true_phrases",
        "authenticity_concerns",
    ],
    "property": [
        "urgency_phrases",
        "payment_red_flags",
        "offsite_patterns",
        "property_specific",
    ],
    "fashion": [
        "urgency_phrases",
        "payment_red_flags",
        "offsite_patterns",
        "authenticity_concerns",
        "too_good_to_be_true_phrases",
    ],
    "general": [
        "urgency_phrases",
        "payment_red_flags",
        "offsite_patterns",
        "too_good_to_be_true_phrases",
    ],
}


# ---------------------------------------------------------------------------
# Core scanning function
# ---------------------------------------------------------------------------

def scan_text_for_patterns(
    text: str,
    category: str = "general",
    include_all_categories: bool = False,
) -> Dict[str, object]:
    """
    Scan listing text for risk indicator patterns and trust signals.

    Performs case-insensitive regex matching against SA marketplace-specific
    pattern libraries. Returns a structured dict of matched patterns and an
    aggregate risk contribution score.

    Args:
        text: Raw listing description or combined listing text to analyse.
        category: Listing category key (e.g. 'vehicle', 'electronics',
                  'property', 'fashion', 'general'). Controls which risk
                  pattern sets are applied.
        include_all_categories: If True, apply all risk pattern sets
                  regardless of category. Useful for comprehensive scans.

    Returns:
        dict with keys:
            matched_risk_patterns  : dict mapping pattern_set -> list of
                                     matched strings
            matched_trust_patterns : dict mapping signal_set -> list of
                                     matched strings
            pattern_risk_score     : int — cumulative risk contribution
                                     from matched patterns (before cap)
            trust_reduction        : int — cumulative trust reduction
            net_pattern_score      : int — pattern_risk_score minus
                                     trust_reduction (floored at 0)
            risk_pattern_count     : int — total number of risk pattern hits
            trust_signal_count     : int — total number of trust signal hits
            applicable_categories  : list of pattern set names applied
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    normalised = text.lower()

    # Determine which risk pattern sets to apply
    resolved_category = category if category in CATEGORY_PATTERN_SETS else "general"
    applicable_sets: List[str] = (
        list(SA_RISK_PATTERNS.keys())
        if include_all_categories
        else CATEGORY_PATTERN_SETS[resolved_category]
    )

    # --- Scan risk patterns ---
    matched_risk: Dict[str, List[str]] = {}
    pattern_risk_score = 0
    risk_pattern_count = 0

    for set_name in applicable_sets:
        patterns = SA_RISK_PATTERNS.get(set_name, [])
        hits: List[str] = []
        for pattern in patterns:
            matches = re.findall(pattern, normalised, re.IGNORECASE)
            hits.extend(matches)
        if hits:
            matched_risk[set_name] = list(set(hits))
            weight = PATTERN_RISK_WEIGHTS.get(set_name, 10)
            # Score each unique pattern match, but cap contribution per set
            # to prevent a single category from dominating the score
            pattern_risk_score += min(weight * len(matched_risk[set_name]), weight * 3)
            risk_pattern_count += len(matched_risk[set_name])

    # --- Scan trust patterns ---
    matched_trust: Dict[str, List[str]] = {}
    trust_reduction = 0
    trust_signal_count = 0

    for set_name, patterns in LEGITIMATE_TRUST_PATTERNS.items():
        hits = []
        for pattern in patterns:
            matches = re.findall(pattern, normalised, re.IGNORECASE)
            hits.extend(matches)
        if hits:
            matched_trust[set_name] = list(set(hits))
            reduction = TRUST_SIGNAL_REDUCTIONS.get(set_name, 5)
            trust_reduction += min(reduction * len(matched_trust[set_name]), reduction * 3)
            trust_signal_count += len(matched_trust[set_name])

    net_score = max(0, pattern_risk_score - trust_reduction)

    return {
        "matched_risk_patterns": matched_risk,
        "matched_trust_patterns": matched_trust,
        "pattern_risk_score": pattern_risk_score,
        "trust_reduction": trust_reduction,
        "net_pattern_score": net_score,
        "risk_pattern_count": risk_pattern_count,
        "trust_signal_count": trust_signal_count,
        "applicable_categories": applicable_sets,
    }


def get_human_readable_flags(scan_result: Dict) -> Dict[str, List[str]]:
    """
    Convert raw pattern scan results into human-readable risk flag descriptions.

    Args:
        scan_result: Output dict from scan_text_for_patterns().

    Returns:
        dict with keys:
            risk_flags   : list of human-readable risk indicator labels
            trust_flags  : list of human-readable trust signal labels
    """
    risk_labels = {
        "urgency_phrases": "Urgency language detected in listing",
        "payment_red_flags": "Atypical payment method or advance-payment language present",
        "offsite_patterns": "Off-platform contact request detected",
        "too_good_to_be_true_phrases": "Unsubstantiated condition claims present",
        "vehicle_specific": "Vehicle documentation or provenance anomaly detected",
        "electronics_specific": "Electronics identification or condition anomaly detected",
        "property_specific": "Property or rental transaction anomaly detected",
        "authenticity_concerns": "Product authenticity verification recommended",
    }
    trust_labels = {
        "positive_seller_signals": "Transparency and in-person verification signals present",
        "transparent_pricing_signals": "Clear and transparent pricing language detected",
        "legitimate_payment_signals": "Standard payment arrangement language present",
    }

    risk_flags = [
        risk_labels.get(k, f"Risk indicator group: {k}")
        for k in scan_result.get("matched_risk_patterns", {})
    ]
    trust_flags = [
        trust_labels.get(k, f"Trust signal group: {k}")
        for k in scan_result.get("matched_trust_patterns", {})
    ]
    return {"risk_flags": risk_flags, "trust_flags": trust_flags}
