-- Membuat replication user khusus yang digunakan oleh replica untuk terhubung ke primary.
CREATE ROLE replicator
  WITH REPLICATION LOGIN
  ENCRYPTED PASSWORD 'replicator_password';
