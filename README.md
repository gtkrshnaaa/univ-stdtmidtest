This repository is presented in Indonesian

# Repositori Ujian Tengah Semester – Sistem Terdistribusi dan Terdesentralisasi

Mata kuliah ini diampu oleh **Dr. Bambang Purnomosidi Dwi Putranto, S.E., Akt., S.Kom., MMSI** ([https://github.com/bpdp](https://github.com/bpdp)).

---

### Identitas Mahasiswa

Nama: **Gilang Teja Krishna**
NIM: **225410001**

---

Repositori ini berisi jawaban Ujian Tengah Semester (UTS) untuk mata kuliah **Sistem Terdistribusi dan Terdesentralisasi**. Seluruh jawaban ditulis dalam Bahasa Indonesia menggunakan format Markdown dan diorganisasikan per soal.

Di dalam repositori ini dosen dapat menemukan:

- Penjelasan konseptual mengenai **Teorema CAP** dan **BASE**, beserta contoh penerapannya.
- Penjelasan mengenai hubungan antara **GraphQL** dan **inter-process communication (IPC)** dalam arsitektur *distributed system*.
- Contoh konfigurasi **PostgreSQL streaming replication** menggunakan **Docker Compose** beserta langkah-langkah eksekusinya dan penjelasan mekanisme sinkronisasi.

---

## Ringkasan soal dan lokasi jawaban

### Soal 1 – Teorema CAP, BASE, dan keterkaitannya

**Perintah soal:**
> Jelaskan teorema CAP dan BASE dan keterkaitan keduanya. Jelaskan menggunakan contoh yang pernah anda gunakan.

**Isi jawaban (ringkas):**

- Menjelaskan kembali definisi **Consistency (C)**, **Availability (A)**, dan **Partition tolerance (P)**.
- Menguraikan karakteristik sistem **CP**, **AP**, dan konteks di mana **CA** hanya bersifat ideal.
- Menjelaskan konsep **BASE** (Basically Available, Soft state, Eventual consistency) serta perbedaannya dengan **ACID**.
- Menjelaskan keterkaitan CAP dan BASE, termasuk bagaimana sistem nyata sering kali bersifat hibrida (sebagian CP, sebagian AP/BASE).
- Memberikan contoh aplikasi Python terdistribusi sederhana (REST API + PostgreSQL + Redis cache) yang memperlihatkan kompromi CAP dan BASE.

**Lokasi file jawaban:**  
[`q1-cap-base/README.md`](q1-cap-base/README.md)

---

### Soal 2 – GraphQL dan komunikasi antar proses pada sistem terdistribusi

**Perintah soal:**
> Jelaskan keterkaitan antara GraphQL dengan komunikasi antar proses pada sistem terdistribusi. Buat diagramnya.

**Isi jawaban (ringkas):**

- Menjelaskan peran **GraphQL** sebagai *API gateway* / *API facade* di depan beberapa **backend service** dalam arsitektur *microservice*.
- Menguraikan bagaimana setiap **resolver** di GraphQL pada praktiknya melakukan **inter-process communication (IPC)** ke service lain, baik secara **synchronous** (HTTP/gRPC) maupun **asynchronous** (message queue, event stream).
- Menjelaskan bahwa dari sudut pandang klien, satu GraphQL query dapat di-*fan-out* menjadi banyak panggilan ke backend, lalu digabung menjadi satu respons JSON.
- Menyertakan dua diagram **Mermaid**:
  - Component diagram: hubungan antara *Client Application*, *GraphQL API Gateway*, dan beberapa *backend service* beserta database-nya.
  - Sequence diagram: alur satu GraphQL query yang memanggil beberapa service (user, order, inventory) melalui IPC.
- Menjelaskan manfaat penggunaan GraphQL di atas IPC: aggregation, client-driven data selection, schema sebagai kontrak, decoupling, serta optimisasi performa.

**Lokasi file jawaban:**  
[`q2-graphql-ipc/README.md`](q2-graphql-ipc/README.md)

---

### Soal 3 – PostgreSQL Streaming Replication dengan Docker Compose

**Perintah soal:**
> Dengan menggunakan Docker / Docker Compose, buatlah streaming replication di PostgreSQL yang bisa menjelaskan sinkronisasi. Tulislah langkah-langkah pengerjaannya dan buat penjelasan secukupnya.

**Isi jawaban (ringkas):**

- Menyusun contoh arsitektur minimal yang terdiri dari dua container PostgreSQL:
  - `postgres-primary` sebagai server **primary** (read/write).
  - `postgres-replica` sebagai server **standby** (read-only) yang menerima **WAL stream** dari primary.
- Menjelaskan berkas-berkas yang digunakan:
  - `docker-compose.yml` (definisi service primary dan replica).
  - `primary/init-primary.sql` (pembuatan replication user).
  - `primary/init-replication.sh` (pengaturan `pg_hba.conf` agar replica dapat terhubung untuk replikasi).
  - `replica/init-replica.sh` (proses `pg_basebackup` dari primary dan konfigurasi standby mode).
- Memberikan langkah-langkah terperinci untuk:
  - Menjalankan klaster dengan Docker Compose.
  - Terhubung ke primary, membuat tabel uji, dan melakukan `INSERT`.
  - Mengecek bahwa data yang sama muncul pada replica.
  - Menghentikan cluster serta menghapus volume bila ingin mengulang dari awal.
- Menjelaskan cara kerja **streaming replication** di PostgreSQL:
  - Peran **write-ahead logging (WAL)**.
  - Perbedaan **asynchronous** dan **synchronous replication**.
  - Jalur sinkronisasi (write path dan read path) dan cara mengamati status replikasi menggunakan `pg_stat_replication`.

**Lokasi file jawaban dan konfigurasi:**  
[`q3-postgres-streaming-replication/README.md`](q3-postgres-streaming-replication/README.md)  
[`q3-postgres-streaming-replication/docker-compose.yml`](q3-postgres-streaming-replication/docker-compose.yml)

---

## Cara menjalankan demo PostgreSQL streaming replication (Soal 3)

Untuk mempermudah pemeriksaan, berikut ringkasan cara menjalankan demo streaming replication yang digunakan pada jawaban Soal 3.

1. Masuk ke direktori konfigurasi:

   ```bash
   cd q3-postgres-streaming-replication
   ```

2. Jalankan service menggunakan Docker Compose:

   ```bash
   docker compose up -d
   ```

   Jika Docker masih menggunakan plugin lama, dapat digunakan:

   ```bash
   docker-compose up -d
   ```

3. Ikuti langkah-langkah yang dijelaskan lebih rinci dalam  
   [`q3-postgres-streaming-replication/README.md`](q3-postgres-streaming-replication/README.md)  
   untuk:

   - Terhubung ke primary dan memasukkan data contoh.
   - Mengecek data yang sama pada replica.
   - Mengamati status replikasi melalui `pg_stat_replication`.

4. Untuk menghentikan dan membersihkan:

   ```bash
   docker compose down        # menghentikan container saja
   docker compose down -v     # menghentikan container dan menghapus volume data
   ```

Dengan struktur dan penjelasan ini, dosen dapat langsung menelusuri setiap jawaban soal beserta konfigurasi yang digunakan hanya dengan mengikuti tautan-tautan di atas.

