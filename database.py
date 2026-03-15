"""
DealScout – PostgreSQL Database Layer
DHD Data | Clients First. Perfection Always.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "dealscout"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create all tables if they don't exist."""
    sql = """
    -- Marketplaces registry
    CREATE TABLE IF NOT EXISTS marketplaces (
        id          SERIAL PRIMARY KEY,
        name        VARCHAR(100) UNIQUE NOT NULL,
        base_url    TEXT NOT NULL,
        active      BOOLEAN DEFAULT TRUE,
        created_at  TIMESTAMP DEFAULT NOW()
    );

    -- Deal categories
    CREATE TABLE IF NOT EXISTS categories (
        id          SERIAL PRIMARY KEY,
        name        VARCHAR(100) UNIQUE NOT NULL,
        icon        VARCHAR(10) DEFAULT '🏷️'
    );

    -- Core deals table
    CREATE TABLE IF NOT EXISTS deals (
        id              SERIAL PRIMARY KEY,
        marketplace_id  INT REFERENCES marketplaces(id),
        category_id     INT REFERENCES categories(id),
        title           TEXT NOT NULL,
        description     TEXT,
        price           NUMERIC(12,2),
        original_price  NUMERIC(12,2),
        currency        VARCHAR(10) DEFAULT 'USD',
        discount_pct    NUMERIC(5,2),
        url             TEXT,
        image_url       TEXT,
        location        VARCHAR(255),
        seller          VARCHAR(255),
        condition       VARCHAR(50) DEFAULT 'Unknown',
        status          VARCHAR(20) DEFAULT 'active',
        scraped_at      TIMESTAMP DEFAULT NOW(),
        expires_at      TIMESTAMP,
        raw_data        JSONB
    );

    -- Scrape jobs log
    CREATE TABLE IF NOT EXISTS scrape_jobs (
        id              SERIAL PRIMARY KEY,
        marketplace_id  INT REFERENCES marketplaces(id),
        status          VARCHAR(20) DEFAULT 'pending',
        deals_found     INT DEFAULT 0,
        deals_new       INT DEFAULT 0,
        errors          TEXT,
        started_at      TIMESTAMP DEFAULT NOW(),
        finished_at     TIMESTAMP
    );

    -- Price alerts
    CREATE TABLE IF NOT EXISTS alerts (
        id              SERIAL PRIMARY KEY,
        keyword         VARCHAR(255) NOT NULL,
        max_price       NUMERIC(12,2),
        category_id     INT REFERENCES categories(id),
        marketplace_id  INT REFERENCES marketplaces(id),
        active          BOOLEAN DEFAULT TRUE,
        created_at      TIMESTAMP DEFAULT NOW()
    );

    -- Seed default marketplaces
    INSERT INTO marketplaces (name, base_url) VALUES
        ('eBay',               'https://www.ebay.com'),
        ('Facebook Marketplace','https://www.facebook.com/marketplace'),
        ('Gumtree',            'https://www.gumtree.com'),
        ('Craigslist',         'https://craigslist.org'),
        ('Amazon',             'https://www.amazon.com')
    ON CONFLICT (name) DO NOTHING;

    -- Seed default categories
    INSERT INTO categories (name, icon) VALUES
        ('Electronics',   '📱'),
        ('Vehicles',      '🚗'),
        ('Furniture',     '🛋️'),
        ('Clothing',      '👗'),
        ('Tools',         '🔧'),
        ('Sports',        '⚽'),
        ('Books',         '📚'),
        ('Gaming',        '🎮'),
        ('Collectibles',  '🏆'),
        ('Other',         '📦')
    ON CONFLICT (name) DO NOTHING;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("✅ Database initialised successfully.")


# ── Query helpers ─────────────────────────────────────────────────────────────

def fetch_deals(limit=100, marketplace=None, category=None, max_price=None,
                search=None, sort_by="scraped_at"):
    conditions = ["d.status = 'active'"]
    params = []

    if marketplace:
        conditions.append("m.name = %s")
        params.append(marketplace)
    if category:
        conditions.append("c.name = %s")
        params.append(category)
    if max_price:
        conditions.append("d.price <= %s")
        params.append(max_price)
    if search:
        conditions.append("d.title ILIKE %s")
        params.append(f"%{search}%")

    where = "WHERE " + " AND ".join(conditions)
    order = f"ORDER BY d.{sort_by} DESC" if sort_by in ("scraped_at","price","discount_pct") else "ORDER BY d.scraped_at DESC"
    params.append(limit)

    sql = f"""
        SELECT d.*, m.name AS marketplace, c.name AS category, c.icon AS cat_icon
        FROM deals d
        LEFT JOIN marketplaces m ON d.marketplace_id = m.id
        LEFT JOIN categories   c ON d.category_id   = c.id
        {where}
        {order}
        LIMIT %s
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def fetch_stats():
    sql = """
        SELECT
            (SELECT COUNT(*) FROM deals WHERE status='active')         AS total_deals,
            (SELECT COUNT(*) FROM deals
             WHERE scraped_at > NOW() - INTERVAL '24 hours')          AS deals_24h,
            (SELECT COUNT(*) FROM marketplaces WHERE active=TRUE)      AS active_marketplaces,
            (SELECT ROUND(AVG(discount_pct),1) FROM deals
             WHERE discount_pct IS NOT NULL AND status='active')       AS avg_discount,
            (SELECT COUNT(*) FROM scrape_jobs
             WHERE started_at > NOW() - INTERVAL '24 hours')          AS jobs_today,
            (SELECT COUNT(*) FROM alerts WHERE active=TRUE)            AS active_alerts
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchone()


def fetch_marketplace_stats():
    sql = """
        SELECT m.name, m.active,
               COUNT(d.id)              AS deal_count,
               ROUND(AVG(d.price), 2)  AS avg_price,
               MAX(d.scraped_at)       AS last_scraped
        FROM marketplaces m
        LEFT JOIN deals d ON d.marketplace_id = m.id AND d.status='active'
        GROUP BY m.id, m.name, m.active
        ORDER BY deal_count DESC
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()


def fetch_price_trend(days=7):
    sql = """
        SELECT DATE(scraped_at) AS day, ROUND(AVG(price),2) AS avg_price,
               COUNT(*) AS deal_count
        FROM deals
        WHERE scraped_at > NOW() - INTERVAL '%s days' AND status='active'
        GROUP BY day ORDER BY day
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (days,))
            return cur.fetchall()


def insert_deal(data: dict):
    sql = """
        INSERT INTO deals
            (marketplace_id, category_id, title, description, price,
             original_price, currency, discount_pct, url, image_url,
             location, seller, condition, raw_data)
        VALUES
            (%(marketplace_id)s, %(category_id)s, %(title)s, %(description)s,
             %(price)s, %(original_price)s, %(currency)s, %(discount_pct)s,
             %(url)s, %(image_url)s, %(location)s, %(seller)s,
             %(condition)s, %(raw_data)s)
        RETURNING id
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, data)
            return cur.fetchone()[0]
        conn.commit()


def log_scrape_job(marketplace_id, status, deals_found=0, deals_new=0, errors=None):
    sql = """
        INSERT INTO scrape_jobs (marketplace_id, status, deals_found, deals_new, errors, finished_at)
        VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING id
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (marketplace_id, status, deals_found, deals_new, errors))
            job_id = cur.fetchone()[0]
        conn.commit()
    return job_id


def fetch_recent_jobs(limit=20):
    sql = """
        SELECT sj.*, m.name AS marketplace
        FROM scrape_jobs sj
        LEFT JOIN marketplaces m ON sj.marketplace_id = m.id
        ORDER BY sj.started_at DESC
        LIMIT %s
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()


def upsert_alert(keyword, max_price=None, category_id=None, marketplace_id=None):
    sql = """
        INSERT INTO alerts (keyword, max_price, category_id, marketplace_id)
        VALUES (%s, %s, %s, %s)
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (keyword, max_price, category_id, marketplace_id))
        conn.commit()


def fetch_alerts():
    sql = """
        SELECT a.*, c.name AS category, m.name AS marketplace
        FROM alerts a
        LEFT JOIN categories c ON a.category_id = c.id
        LEFT JOIN marketplaces m ON a.marketplace_id = m.id
        WHERE a.active = TRUE ORDER BY a.created_at DESC
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()


if __name__ == "__main__":
    init_db()
