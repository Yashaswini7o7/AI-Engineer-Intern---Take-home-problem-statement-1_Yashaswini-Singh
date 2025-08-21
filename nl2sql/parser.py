"""
Rule-based NL→SQL parser.
Covers the provided CXO-style questions and common variants.
Easy to extend: add new 'if' blocks or helper functions.
"""
import re
from datetime import datetime

CITIES = ["london", "bradford"]
PROPERTY_TYPES = ["apartment", "house", "studio", "villa", "apartments", "houses"]
CURRENCY = r"[\$\£\€]?"

def _clean(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def _extract_city(q: str):
    for c in CITIES:
        if c in q:
            return c.capitalize()
    
    m = re.search(r"in ([a-zA-Z\s]+)", q)
    if m:
        return m.group(1).strip().title()
    return None

def _extract_year(q: str, default_year=None):
    m = re.search(r"(20\d{2})", q)
    if m:
        return int(m.group(1))
    return default_year

def _extract_quarter(q: str):
    m = re.search(r"(q[1-4])\s*(20\d{2})?", q)
    if not m:
        return None, None
    qn = int(m.group(1)[1])
    year = int(m.group(2)) if m.group(2) else datetime.now().year
    return qn, year

def _extract_price(q: str):
    
    m = re.search(r"(under|below|<=|less than)\s*"+CURRENCY+r"\s*([\d,]+)", q)
    if m:
        return float(m.group(2).replace(",", ""))
    m = re.search(CURRENCY+r"\s*([\d,]+)", q)  # fallback: any number mentioned
    if m:
        return float(m.group(1).replace(",", ""))
    return None

def _is_2bhk(q: str):
    return "2bhk" in q or re.search(r"\b2\s*bed(room)?s?\b", q) is not None

def _plural_to_singular(pt: str) -> str:
    return {"apartments": "apartment", "houses": "house"}.get(pt, pt)

def nl_to_sql(question: str) -> str | None:
    """
    Map natural language question -> SQL string.
    Returns None when unable to parse (triggers graceful fallback).
    """
    q = _clean(question.lower())

    # Top tenants by total rent paid
    if ("top" in q and "tenant" in q and ("rent" in q or "amount" in q)) or \
       ("tenants" in q and "total rent" in q):
        # default top 10
        lim = 10
        m = re.search(r"top\s+(\d+)", q)
        if m:
            lim = int(m.group(1))
        return f"""
        SELECT py.tenant_id, SUM(py.amount) AS total_rent
        FROM payments py
        WHERE py.status = 'successful'
        GROUP BY py.tenant_id
        ORDER BY total_rent DESC
        LIMIT {lim};
        """

    # Average rating apartments vs houses
    if "average rating" in q and ("apartment" in q or "house" in q or "vs" in q):
        return """
        SELECT p.property_type, ROUND(AVG(r.rating), 2) AS avg_rating
        FROM reviews r
        JOIN properties p ON p.property_id = r.property_id
        WHERE p.property_type IN ('apartment','house')
        GROUP BY p.property_type
        ORDER BY p.property_type;
        """

    # Landlords by revenue in a given year
    if ("landlord" in q and ("revenue" in q or "earnings" in q)) or \
       ("most revenue" in q and "landlord" in q):
        year = _extract_year(q, default_year=datetime.now().year)
        return f"""
        SELECT (u.first_name || ' ' || u.last_name) AS landlord, 
               ROUND(SUM(py.amount), 2) AS revenue
        FROM payments py
        JOIN bookings b  ON b.booking_id = py.booking_id
        JOIN properties p ON p.property_id = b.property_id
        JOIN users u      ON u.user_id = p.landlord_id
        WHERE py.status = 'successful'
          AND strftime('%Y', py.payment_date) = '{year}'
        GROUP BY landlord
        ORDER BY revenue DESC;
        """

    # Availability: 2BHK under price in city
    if ("available" in q or "currently available" in q) and _is_2bhk(q):
        city = _extract_city(q) or "London"
        price = _extract_price(q) or 2500
        return f"""
        SELECT p.title, p.city, p.bedrooms, p.rent_price, p.status
        FROM properties p
        WHERE p.status='available'
          AND p.bedrooms=2
          AND p.city = '{city}'
          AND p.rent_price < {price}
        ORDER BY p.rent_price ASC;
        """

    # Occupancy rate for a city in a specific quarter/year

    if ("occupancy rate" in q or "occupancy" in q) and ("quarter" in q or "q" in q):
        city = _extract_city(q) or "Bradford"
        qn, year = _extract_quarter(q)
        if not qn:
            
            return None
        quarter_months = {1: ("01","03"), 2: ("04","06"), 3: ("07","09"), 4: ("10","12")}
        m1, m3 = quarter_months[qn]
        start = f"{year}-{m1}-01"
        end = {
            "03": f"{year}-03-31", "06": f"{year}-06-30",
            "09": f"{year}-09-30", "12": f"{year}-12-31"
        }[m3]
        return f"""
        WITH city_props AS (
          SELECT property_id FROM properties WHERE city = '{city}'
        ),
        quarter_bookings AS (
          SELECT b.property_id,
                 MAX(date(b.start_date, 'start of day')) AS s,
                 MAX(date(b.end_date, 'start of day'))   AS e
          FROM bookings b
          JOIN city_props cp ON cp.property_id = b.property_id
          WHERE NOT (b.end_date < date('{start}') OR b.start_date > date('{end}'))
            AND b.status IN ('confirmed','completed')
          GROUP BY b.booking_id
        ),
        span AS (
          SELECT COUNT(*) AS prop_count FROM city_props
        ),
        booked_days AS (
          SELECT SUM(
            JULIANDAY(
              CASE WHEN e > date('{end}') THEN date('{end}') ELSE e END
            ) - JULIANDAY(
              CASE WHEN s < date('{start}') THEN date('{start}') ELSE s END
            ) + 1
          ) AS booked
          FROM quarter_bookings
        ),
        denom AS (
          SELECT prop_count * 
                 (JULIANDAY('{end}') - JULIANDAY('{start}') + 1) AS total_days
          FROM span
        )
        SELECT 
          '{city}' AS city,
          'Q{qn} {year}' AS period,
          ROUND(100.0 * COALESCE(b.booked,0) / NULLIF(d.total_days,0), 2) AS occupancy_rate_percent
        FROM booked_days b, denom d;
        """.format(qn=qn, year=year, city=city)


    return None
