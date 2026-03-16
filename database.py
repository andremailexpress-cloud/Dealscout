"""
Deal Hunter Pro X — Supabase Database Layer
DHD Data | Clients First. Perfection Always.
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timezone

load_dotenv()

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_ANON_KEY"]
        _client = create_client(url, key)
    return _client


# ── Deals ──────────────────────────────────────────────────────────────────────

def save_deal(deal: dict) -> dict | None:
    """Insert a scraped deal. Returns the saved row or None."""
    result = get_client().table("deals").insert(deal).execute()
    return result.data[0] if result.data else None


def get_active_deals(limit: int = 50, platform: str = None,
                     category: str = None, max_price: float = None) -> list:
    """Fetch active deals with optional filters, ordered by discount."""
    q = (
        get_client().table("deals")
        .select("*")
        .eq("is_active", True)
        .order("discount_pct", desc=True)
        .limit(limit)
    )
    if platform:
        q = q.eq("platform", platform)
    if category:
        q = q.eq("category", category)
    if max_price:
        q = q.lte("price", max_price)
    return q.execute().data or []


def get_smoking_deals() -> list:
    """Deals 35%+ below market price."""
    result = (
        get_client().table("deals")
        .select("*")
        .eq("is_smoking_deal", True)
        .eq("is_active", True)
        .execute()
    )
    return result.data or []


def expire_old_deals():
    """Mark deals past their expiry as inactive."""
    now = datetime.now(timezone.utc).isoformat()
    get_client().table("deals").update({"is_active": False}).lt("expires_at", now).execute()


# ── Scrape Jobs ────────────────────────────────────────────────────────────────

def log_scrape_job(platform: str) -> str | None:
    """Create a running scrape job entry. Returns job id."""
    result = (
        get_client().table("scrape_jobs")
        .insert({"platform": platform, "status": "running"})
        .execute()
    )
    return result.data[0]["id"] if result.data else None


def finish_scrape_job(job_id: str, deals_found: int,
                      status: str = "success", error: str = None):
    """Update scrape job on completion."""
    payload = {
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "deals_found": deals_found,
        "status": status,
    }
    if error:
        payload["error_msg"] = error
    get_client().table("scrape_jobs").update(payload).eq("id", job_id).execute()


def get_recent_jobs(limit: int = 20) -> list:
    result = (
        get_client().table("scrape_jobs")
        .select("*")
        .order("started_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


# ── Connection test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        jobs = get_recent_jobs(1)
        print("OK: Supabase connection successful.")
    except Exception as e:
        print(f"FAILED: {e}")
