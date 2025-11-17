## Soal 1 – Teorema CAP, BASE, dan Keterkaitannya

## 1. Teorema CAP

Teorema **CAP** menjelaskan kompromi mendasar yang dihadapi *distributed data store* ketika terjadi *network partition*. Secara ringkas, teorema ini menyatakan bahwa dalam kondisi terjadi *partition*, sebuah *distributed system* hanya dapat menjamin **paling banyak dua** dari tiga properti berikut secara bersamaan:

- **Consistency (C)** – Setiap operasi baca (*read*) selalu menerima hasil tulis (*write*) yang paling mutakhir, atau mendapatkan error. Dari sudut pandang klien, sistem berperilaku seolah-olah hanya ada satu *node* yang selalu up-to-date (sering diformalkan sebagai *linearizability*).
- **Availability (A)** – Setiap permintaan mendapatkan respons non-error, tanpa mensyaratkan semua *node* berada dalam keadaan up-to-date. Setiap *node* yang tidak gagal dapat merespons secara mandiri.
- **Partition tolerance (P)** – Sistem tetap dapat beroperasi meskipun terjadi kegagalan jaringan yang membagi *node-node* menjadi beberapa kelompok yang tidak dapat saling berkomunikasi secara penuh.

Dalam lingkungan terdistribusi di dunia nyata, **network partition hampir tidak dapat dihindari**, sehingga kita harus mengasumsikan keberadaan **P**. Ketika *partition* terjadi, perancang sistem harus memilih antara:

- **CP (Consistent and Partition-tolerant)** – Mengorbankan *availability* ketika terjadi *partition*.
- **AP (Available and Partition-tolerant)** – Mengorbankan *strong consistency* ketika terjadi *partition*.

### 1.1 Consistent and Partition-tolerant (CP)

Sistem **CP** memprioritaskan *strong consistency* dibandingkan *availability* ketika terjadi *partition*. Perilaku yang umum dijumpai:

- Jika suatu *node* tidak dapat menghubungi *quorum* atau *leader*, *node* tersebut akan menolak operasi baca maupun tulis untuk menghindari pengembalian data yang sudah usang.
- Klien dapat mengalami error atau *timeout*, tetapi data yang diterima dan disimpan oleh sistem tetap konsisten secara kuat.

Contoh secara konseptual:

- *Replicated configuration store* atau layanan koordinasi (misalnya sistem yang dibangun di atas algoritma konsensus seperti **Raft** atau **Paxos**), di mana kebenaran data lebih penting dibandingkan *availability*.

### 1.2 Available and Partition-tolerant (AP)

Sistem **AP** memprioritaskan *availability*. Ketika terjadi *partition*:

- Setiap *partition* tetap dapat menerima permintaan.
- Keadaan data di masing-masing *partition* dapat sementara menyimpang satu sama lain.
- Sistem mengandalkan proses **reconciliation** dan **eventual convergence** setelah *partition* pulih untuk menyamakan kembali keadaan data.

Contoh secara konseptual:

- *Key-value store* bergaya **Dynamo** dan banyak sistem NoSQL berskala besar yang menerima *write* pada beberapa replika sekaligus, kemudian melakukan *conflict resolution* untuk menyatukan perbedaan.

### 1.3 CA (Consistent and Available)

Sistem **CA** bersifat konsisten dan tersedia selama **tidak terjadi partition**. Dalam lingkungan terdistribusi yang realistis, CA biasanya merupakan kasus ideal (misalnya sebuah *single-node database* atau klaster pada jaringan yang diasumsikan tidak pernah mengalami kegagalan). Ketika kita menerima kenyataan bahwa *partition* dapat terjadi, maka kita harus melepaskan salah satu dari C atau A dalam kondisi tersebut.

---

## 2. BASE: Basically Available, Soft state, Eventual consistency

**BASE** adalah filosofi perancangan yang banyak digunakan pada *large-scale distributed systems* yang lebih mengutamakan *availability* dan *partition tolerance*. BASE sering dipandang sebagai pasangan alternatif dari **ACID** dalam konteks *highly available data store*.

BASE merupakan akronim dari:

- **Basically Available** – Sistem berupaya tetap responsif dan mampu menerima permintaan sebagian besar waktu, bahkan ketika terjadi kegagalan parsial maupun *partition*. Respons yang diberikan dapat berupa data yang sudah agak usang atau pendekatan (*approximation*).
- **Soft state** – Keadaan sistem dapat berubah dari waktu ke waktu meskipun tidak ada input baru dari klien. Hal ini terjadi karena adanya replikasi asinkron dan proses rekonsiliasi di latar belakang yang memperbarui replika.
- **Eventual consistency** – Jika tidak ada pembaruan baru, semua replika pada akhirnya akan berkumpul pada keadaan yang sama. Tidak ada jaminan bahwa setiap *read* selalu mengembalikan *write* paling mutakhir, tetapi sistem menjamin konvergensi dalam jangka waktu tertentu.

Sebagai perbandingan, **ACID** (Atomicity, Consistency, Isolation, Durability) menekankan semantik transaksi yang ketat, yang relatif lebih mudah dijamin pada *single node* atau sistem CP yang **strongly consistent**, tetapi menjadi semakin sulit bila ingin diskalakan tanpa mengorbankan *high availability* lintas *partition*.

---

## 3. Keterkaitan antara CAP dan BASE

Teorema **CAP** merupakan **batas teoretis** mengenai apa yang mungkin dicapai oleh *distributed system* ketika terjadi *partition*. Sementara itu, **BASE** adalah **pendekatan praktis** yang secara eksplisit memihak sisi **AP** dari CAP:

- Sistem yang memilih **AP** dalam kerangka CAP sering kali menerapkan prinsip-prinsip **BASE**.
- Alih-alih memblokir atau menolak permintaan selama terjadi *partition* (perilaku CP), sistem yang menganut BASE cenderung:
  - Menerima *write* secara lokal.
  - Mengizinkan adanya perbedaan sementara antar replika.
  - Mengandalkan replikasi asinkron dan mekanisme *conflict resolution* untuk mencapai konvergensi.

Dengan demikian:

- **CAP** menyatakan bahwa *strong consistency*, *availability*, dan *partition tolerance* tidak dapat dicapai semuanya secara penuh sekaligus.
- **BASE** menggambarkan salah satu gaya perancangan yang secara sadar menerima **konsistensi yang lebih lemah** (*eventual consistency*) demi memperoleh *availability* dan toleransi kegagalan yang lebih tinggi.

Dalam praktik, banyak arsitektur nyata yang bersifat **hibrida**:

- Beberapa subsistem atau operasi dirancang dengan sifat **CP** (misalnya penyimpanan konfigurasi kritis atau *ledger* yang memerlukan *strong consistency*).
- Subsistem lain cenderung **AP/BASE** (misalnya *caching*, *analytics*, *feed timeline*) di mana data yang agak usang masih dapat diterima untuk sementara waktu.

---

## 4. Contoh dari aplikasi Python terdistribusi sederhana

Dalam mata kuliah ini saya mengerjakan sebuah aplikasi terdistribusi sederhana menggunakan Python yang menyediakan REST API dan menggunakan PostgreSQL bersama sebuah *cache*. Walaupun kode yang digunakan tidak terlalu besar, arsitektur tersebut sudah cukup untuk menggambarkan kompromi CAP dan BASE.

### 4.1 Deskripsi sistem

Secara garis besar, sistem terdiri atas:

- Sebuah **Python API service** (misalnya diimplementasikan dengan FastAPI atau Flask) yang dijalankan dalam beberapa *instance* di belakang sebuah *load balancer*.
- Sebuah **PostgreSQL database** yang berperan sebagai *primary store* untuk penyimpanan data pengguna yang bersifat durabel.
- Sebuah **Redis cache** yang digunakan untuk mempercepat *read-heavy endpoint* (misalnya pengambilan profil pengguna atau detail produk) dengan cara menyimpan tampilan data yang sudah didenormalisasi atau hasil perhitungan sebelumnya.

Instance API dan Redis dijalankan pada *container* yang terpisah, dan PostgreSQL juga berjalan pada *container* tersendiri. Semua *container* saling berkomunikasi melalui *virtual network* yang disediakan oleh Docker.

Alur tipikal untuk permintaan baca (*read request*):

1. Klien memanggil endpoint pada API.
2. API terlebih dahulu memeriksa Redis untuk mencari *key* yang sesuai.
3. Jika *key* ditemukan, API mengembalikan nilai yang ada di *cache*.
4. Jika *key* tidak ditemukan, API melakukan query ke PostgreSQL, mengembalikan hasilnya kepada klien, lalu memperbarui *cache* secara asinkron.

### 4.2 Kompromi CAP pada sistem ini

Jika terjadi **network partition** antara *instance* API dan PostgreSQL, kita harus memutuskan bagaimana menangani operasi tulis (*write*):

- Perilaku **CP**: Menolak *write* ketika database tidak dapat dijangkau untuk menghindari kehilangan data atau terjadinya divergensi antar replika. Sistem tetap konsisten, tetapi tidak sepenuhnya tersedia.
- Perilaku **AP/BASE**: Menerima *write* sementara ke media penyimpanan lain (misalnya *in-memory queue* atau log lokal) dan memutar ulang (*replay*) *write* tersebut ketika *partition* sudah pulih. Selama *partition* berlangsung, *instance* API yang berbeda mungkin melihat keadaan data yang berbeda, tetapi sistem tetap tersedia.

Dalam aplikasi sederhana yang saya kerjakan, perilaku yang dipilih untuk operasi tulis lebih dekat ke **CP**:

- Ketika PostgreSQL tidak tersedia, API mengembalikan error daripada menerima *write* baru yang tidak dapat dipastikan tersimpan secara durabel.
- Artinya, kami memprioritaskan **strong consistency** untuk data yang durabel dibandingkan *availability*.

Namun, untuk operasi baca kami menerima perilaku yang lebih mendekati **BASE** dengan memanfaatkan Redis:

- Data yang tersimpan di *cache* dapat menjadi **stale** apabila baris data di PostgreSQL telah berubah tetapi *cache* belum diperbarui.
- Sistem tetap **basically available**: API masih dapat merespons permintaan dengan menggunakan *cache* meskipun terdapat keterlambatan dalam propagasi pembaruan.
- Keadaan *cache* bersifat **soft state**: proses di latar belakang atau mekanisme invalidasi *cache* akan memperbaruinya dari waktu ke waktu.
- Secara keseluruhan, sistem mencapai **eventual consistency**: setelah beberapa saat, nilai di *cache* akan kembali selaras dengan data di PostgreSQL.

### 4.3 Manifestasi CAP dan BASE dalam contoh ini

- Untuk data yang bersifat **durable dan authoritative** di PostgreSQL, sistem berperilaku mendekati **CP**. Pada kegagalan yang serius, lebih baik mengembalikan error daripada menerima *write* yang berpotensi hilang.
- Untuk kebutuhan **kinerja baca dan pengalaman pengguna**, kami menambahkan lapisan *cache* bergaya **BASE** (Redis) yang mengizinkan data sedikit usang namun dapat diakses dengan cepat dan pada akhirnya akan konvergen.

Contoh ini menunjukkan bahwa bahkan pada aplikasi Python terdistribusi yang sederhana sekalipun, kita sudah perlu berpikir dalam kerangka CAP dan BASE:

- Operasi mana yang harus tetap *strongly consistent* ketika terjadi kegagalan (kecenderungan CP)?
- Operasi mana yang dapat mentoleransi *temporary inconsistency* demi memperoleh *availability* dan kinerja yang lebih baik (kecenderungan AP/BASE)?

