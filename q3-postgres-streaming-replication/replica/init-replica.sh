#\!/bin/bash
set -e

# Skrip ini dijalankan selama initial database setup pada replica.
# Skrip ini menunggu hingga primary siap, mengosongkan local data
# directory, dan menggunakan pg_basebackup untuk mengkloning data directory
# dari primary serta mengonfigurasi streaming replication.

export PGPASSWORD="replicator_password"

echo "Menunggu primary hingga siap..."
until pg_isready -h postgres-primary -p 5432 -U replicator; do
  echo "Primary belum siap - menunggu..."
  sleep 2
done

echo "Primary sudah siap. Menjalankan base backup..."
rm -rf "$PGDATA"/*

pg_basebackup \
  -h postgres-primary \
  -D "$PGDATA" \
  -U replicator \
  -P \
  -R \
  -X stream

echo "Base backup selesai. Replica akan berjalan dalam standby mode."
