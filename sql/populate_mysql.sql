-- Dummy data for storefront Django project
-- Run this in MySQL Workbench after creating/choosing your database server.

CREATE DATABASE IF NOT EXISTS storefront_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE storefront_db;

-- Disable FK checks while truncating/adding data
SET FOREIGN_KEY_CHECKS = 0;

-- NOTE: adjust table names if your Django DB uses a different table prefix
-- Clear target tables (be careful in production)
TRUNCATE TABLE IF EXISTS tags_taggeditem;
TRUNCATE TABLE IF EXISTS tags_tag;
TRUNCATE TABLE IF EXISTS store_review;
TRUNCATE TABLE IF EXISTS store_address;
TRUNCATE TABLE IF EXISTS store_cartitem;
TRUNCATE TABLE IF EXISTS store_cart;
TRUNCATE TABLE IF EXISTS store_orderitem;
TRUNCATE TABLE IF EXISTS store_order;
TRUNCATE TABLE IF EXISTS store_customer;
TRUNCATE TABLE IF EXISTS store_product_promotions;
TRUNCATE TABLE IF EXISTS store_product;
TRUNCATE TABLE IF EXISTS store_collection;
TRUNCATE TABLE IF EXISTS store_promotion;
TRUNCATE TABLE IF EXISTS auth_user;

SET FOREIGN_KEY_CHECKS = 1;

-- Insert some users (Django auth_user simple fields)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(1, 'pbkdf2_sha256$260000$example1$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', NULL, 0, 'alice', 'Alice', 'Johnson', 'alice@example.com', 0, 1, '2025-01-01 08:00:00'),
(2, 'pbkdf2_sha256$260000$example2$YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', NULL, 0, 'bob', 'Bob', 'Smith', 'bob@example.com', 0, 1, '2025-02-01 09:00:00'),
(3, 'pbkdf2_sha256$260000$example3$ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', NULL, 0, 'carol', 'Carol', 'Nguyen', 'carol@example.com', 1, 1, '2025-03-01 10:00:00'),
(4, 'pbkdf2_sha256$260000$example4$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', NULL, 0, 'dave', 'Dave', 'Lee', 'dave@example.com', 0, 1, '2025-04-01 11:00:00'),
(5, 'pbkdf2_sha256$260000$example5$BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', NULL, 0, 'eve', 'Eve', 'Martinez', 'eve@example.com', 0, 1, '2025-05-01 12:00:00');

-- Promotions
INSERT INTO store_promotion (id, description, discount) VALUES
(1, 'Black Friday 20% off', 20.0),
(2, 'New Year 10% off', 10.0);

-- Collections
INSERT INTO store_collection (id, title, featured_product_id) VALUES
(1, 'Electronics', NULL),
(2, 'Books', NULL),
(3, 'Home & Kitchen', NULL),
(4, 'Sports', NULL);

-- Products
INSERT INTO store_product (id, title, slug, description, price, inventory, last_update, collection_id)
VALUES
(1, 'Wireless Headphones', 'wireless-headphones', 'Bluetooth noise-cancelling headphones', 99.99, 120, NOW(), 1),
(2, 'USB-C Charger 30W', 'usb-c-charger-30w', 'Fast charger for phones and tablets', 19.99, 300, NOW(), 1),
(3, 'Python Programming: Intro', 'python-programming-intro', 'Beginner Python programming book', 29.95, 80, NOW(), 2),
(4, 'Data Science Essentials', 'data-science-essentials', 'Practical guide to data science', 39.50, 50, NOW(), 2),
(5, 'Non-stick Frying Pan', 'non-stick-frying-pan', '10 inch skillet, dishwasher safe', 24.99, 200, NOW(), 3),
(6, 'Ceramic Mug Set', 'ceramic-mug-set', 'Set of 4 coffee mugs', 18.00, 150, NOW(), 3),
(7, 'Yoga Mat 6mm', 'yoga-mat-6mm', 'Non-slip yoga mat', 25.00, 90, NOW(), 4),
(8, 'Stainless Water Bottle', 'stainless-water-bottle', 'Insulated 750ml bottle', 22.00, 140, NOW(), 4),
(9, 'Smart Speaker Mini', 'smart-speaker-mini', 'Voice assistant with high-quality sound', 49.99, 60, NOW(), 1),
(10, 'Wireless Mouse', 'wireless-mouse', 'Ergonomic mouse with USB receiver', 14.99, 220, NOW(), 1);

-- Link product promotions (M2M table name may vary; typical name: store_product_promotions)
INSERT INTO store_product_promotions (id, product_id, promotion_id) VALUES
(1, 1, 1),
(2, 3, 2);

-- Customers (must reference auth_user ids)
INSERT INTO store_customer (id, phone, birth_date, membership, user_id) VALUES
(1, '555-0101', '1990-06-15', 'S', 1),
(2, '555-0202', '1988-02-20', 'B', 2),
(3, '555-0303', '1985-12-05', 'G', 3),
(4, '555-0404', '1992-09-09', 'B', 4),
(5, '555-0505', '1995-03-03', 'B', 5);

-- Addresses
INSERT INTO store_address (id, street, city, customer_id) VALUES
(1, '123 Maple St', 'Springfield', 1),
(2, '45 Oak Ave', 'Seattle', 2),
(3, '900 Elm Rd', 'Austin', 3),
(4, '77 Pine Ln', 'Denver', 4),
(5, '10 Market St', 'San Francisco', 5);

-- Orders
INSERT INTO store_order (id, placed_at, payment_status, customer_id) VALUES
(1, '2025-11-01', 'C', 1),
(2, '2025-11-15', 'P', 2),
(3, '2025-11-20', 'P', 1),
(4, '2025-11-18', 'C', 4),
(5, '2025-11-10', 'C', 5);

-- Order items
INSERT INTO store_orderitem (id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 99.99),
(2, 1, 10, 1, 14.99),
(3, 2, 9, 1, 49.99),
(4, 3, 5, 1, 24.99),
(5, 4, 2, 2, 19.99),
(6, 5, 7, 2, 25.00);

INSERT INTO store_cart (id, created_at) VALUES
(UUID(), NOW()),
(UUID(), NOW());
-- Explicitly insert cart items with UUIDs
-- Example of inserting cart items with explicit UUIDs
INSERT INTO store_cartitem (id, cart_id, product_id, quantity) VALUES 
('cart_uuid_1', 'PUT_CART_UUID_HERE', 2, 1),
('cart_uuid_2', 'PUT_CART_UUID_HERE', 1, 2);
-- Replace 'PUT_CART_UUID_HERE' with actual UUIDs from the store_cart table
-- Ensure to adjust the product_id and quantity as needed

-- Cart items: to insert you must copy the UUID from store_cart table; example placeholders below:
-- INSERT INTO store_cartitem (id, cart_id, product_id, quantity) VALUES (1, 'PUT_CART_UUID_HERE', 2, 1);

-- Reviews
INSERT INTO store_review (id, product_id, name, description, date) VALUES
(1, 1, 'Alice', 'Great sound and battery life.', '2025-11-02'),
(2, 3, 'Bob', 'Good for beginners, clear examples.', '2025-11-16'),
(3, 5, 'Dave', 'Decent pan but handle gets hot.', '2025-11-19'),
(4, 9, 'Bob', 'Compact speaker, surprising bass.', '2025-11-16');

-- Tags (note model field is 'lable' in your tags app)
INSERT INTO tags_tag (id, lable) VALUES
(1, 'electronics'),
(2, 'audio'),
(3, 'kitchen');

-- Example TaggedItem: content_type IDs differ per project; skip adding TaggedItem unless you confirm ContentType ids

-- Quick counts for sanity
SELECT COUNT(*) AS users_count FROM auth_user;
SELECT COUNT(*) AS products_count FROM store_product;
SELECT COUNT(*) AS customers_count FROM store_customer;

-- Done

-- IMPORTANT: After running this script, run your Django `manage.py migrate` and `manage.py check` locally to ensure model/table alignment.
-- If your actual table names differ (e.g. you use a custom DB prefix), adjust the INSERT INTO table names accordingly.
