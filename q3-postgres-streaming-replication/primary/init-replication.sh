#\!/bin/bash
set -e

# Skrip ini dijalankan selama proses initial database setup pada primary.
# Skrip ini menambahkan aturan pada pg_hba.conf yang mengizinkan container replica
# untuk terhubung menggunakan replication user dari seluruh alamat di Docker network.

echo "host replication replicator 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
