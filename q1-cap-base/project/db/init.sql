-- Inisialisasi skema database untuk contoh pada Soal 1 (CAP/BASE).
-- Tabel sederhana untuk menyimpan item yang akan diakses melalui API.

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO items (name, description) VALUES
    ('Item pertama', 'Contoh item yang diinisialisasi saat database dibuat.'),
    ('Item kedua', 'Contoh item kedua untuk pengujian API dan cache.');
