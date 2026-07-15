CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

INSERT INTO items (name, description) VALUES
    ('First item', 'Seeded from init.sql'),
    ('Second item', 'Read from MySQL'),
    ('Third item', 'Served via the API');
