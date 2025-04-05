CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notifications (email, message)
SELECT 'vannessanga24@gmail.com', 'eat 1 panadol'
WHERE NOT EXISTS (
    SELECT 1 FROM notifications WHERE email='vannessanga24@gmail.com' AND message='eat 1 panadol'
);
