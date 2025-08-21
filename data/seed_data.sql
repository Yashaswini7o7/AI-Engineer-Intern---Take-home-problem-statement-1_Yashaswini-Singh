-- Users (landlords + tenants)
INSERT INTO users (user_id, first_name, last_name, email, role) VALUES
(1,'Alice','Smith','alice@l.com','landlord'),
(2,'Bob','Brown','bob@t.com','tenant'),
(3,'Charlie','White','charlie@t.com','tenant'),
(4,'Diana','Green','diana@l.com','landlord');

-- Properties
INSERT INTO properties (property_id, landlord_id, title, description, property_type, address, city, state, country, bedrooms, bathrooms, rent_price, status)
VALUES
(1,1,'Modern Apartment','Near tube','apartment','1A Baker St','London','England','UK',2,1,2000,'available'),
(2,1,'Spacious Villa','Garden view','villa','22 High Rd','Bradford','England','UK',4,3,3500,'booked'),
(3,4,'Cozy House','Great schools','house','7 Elm Ave','London','England','UK',2,2,2200,'available'),
(4,4,'Studio Central','Compact','studio','19 King St','Bradford','England','UK',1,1,1200,'available'),
(5,1,'Family House','Suburban','house','31 Oak Dr','Bradford','England','UK',3,2,1800,'booked');

-- Bookings (2024 focus for test determinism)
INSERT INTO bookings (booking_id, property_id, tenant_id, start_date, end_date, status) VALUES
(1,2,3,'2024-04-05','2024-06-15','completed'),   -- Bradford, Q2 2024
(2,5,2,'2024-04-10','2024-06-05','completed'),   -- Bradford, Q2 2024
(3,1,2,'2024-01-01','2024-03-01','completed'),   -- London, Q1 2024
(4,3,3,'2024-09-01','2024-10-01','confirmed');   -- London, Q3 2024

-- Payments (successful only counted)
INSERT INTO payments (payment_id, booking_id, tenant_id, amount, payment_date, status, method) VALUES
(1,1,3,7000,'2024-06-15','successful','credit_card'),
(2,2,2,5000,'2024-06-05','successful','upi'),
(3,3,2,4000,'2024-03-01','successful','debit_card'),
(4,4,3,2500,'2024-09-01','successful','bank_transfer');

-- Reviews
INSERT INTO reviews (review_id, property_id, tenant_id, rating, comment) VALUES
(1,1,2,5,'Excellent'),
(2,3,3,3,'Okay'),
(3,2,3,4,'Good villa'),
(4,5,2,4,'Nice house');

-- Favorites
INSERT INTO favorites (tenant_id, property_id) VALUES
(2,1),(2,3),(3,2);
