PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS property_photos;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    first_name  TEXT,
    last_name   TEXT,
    email       TEXT UNIQUE,
    phone       TEXT,
    role        TEXT CHECK(role IN ('landlord','tenant','admin')),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE properties (
    property_id   INTEGER PRIMARY KEY,
    landlord_id   INT REFERENCES users(user_id),
    title         TEXT,
    description   TEXT,
    property_type TEXT CHECK(property_type IN ('apartment','house','studio','villa')),
    address       TEXT,
    city          TEXT,
    state         TEXT,
    country       TEXT,
    bedrooms      INT,
    bathrooms     INT,
    rent_price    DECIMAL(12,2),
    status        TEXT CHECK(status IN ('available','booked','inactive')),
    listed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    booking_id  INTEGER PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    tenant_id   INT REFERENCES users(user_id),
    start_date  DATE,
    end_date    DATE,
    status      TEXT CHECK(status IN ('pending','confirmed','cancelled','completed')),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    payment_id   INTEGER PRIMARY KEY,
    booking_id   INT REFERENCES bookings(booking_id),
    tenant_id    INT REFERENCES users(user_id),
    amount       DECIMAL(12,2),
    payment_date DATE,
    status       TEXT CHECK(status IN ('initiated','successful','failed','refunded')),
    method       TEXT CHECK(method IN ('credit_card','debit_card','bank_transfer','upi','cash'))
);

CREATE TABLE reviews (
    review_id   INTEGER PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    tenant_id   INT REFERENCES users(user_id),
    rating      INT,
    comment     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE property_photos (
    photo_id    INTEGER PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    photo_url   TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favorites (
    tenant_id   INT REFERENCES users(user_id),
    property_id INT REFERENCES properties(property_id),
    added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tenant_id, property_id)
);
