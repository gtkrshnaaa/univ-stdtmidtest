import os
import json
from typing import Optional

import psycopg2
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Aplikasi ini merupakan contoh sederhana dari arsitektur pada poin 4 jawaban Soal 1:
# - Python API service
# - PostgreSQL database sebagai primary store
# - Redis cache untuk mempercepat operasi baca (read-heavy endpoint)
# API ini memperlihatkan pola: client -> API -> Redis (cache) -> PostgreSQL (database).

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_user:app_password@db:5432/app_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")


def get_db_connection():
    """Membuat koneksi baru ke PostgreSQL berdasarkan DATABASE_URL.

    Untuk kesederhanaan, contoh ini membuat koneksi per permintaan (request).
    Dalam sistem produksi, sebaiknya menggunakan connection pool.
    """
    return psycopg2.connect(DATABASE_URL)


redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    """Mengembalikan client Redis global.

    Client disiapkan sekali dan digunakan kembali untuk setiap request.
    """
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    source: str


app = FastAPI(
    title="Q1 CAP/BASE Example API",
    description=(
        "Contoh API sederhana untuk menggambarkan kompromi CAP dan BASE "
        "dengan menggunakan PostgreSQL sebagai primary store dan Redis sebagai cache."
    ),
)


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """Mengambil item berdasarkan ID dengan pola cache-aside.

    Langkah-langkah:
    1. API memeriksa Redis terlebih dahulu.
    2. Jika data ada di cache, kembalikan dari cache (source="cache").
    3. Jika tidak ada di cache, API membaca dari PostgreSQL dan menyimpan
       hasilnya ke Redis sebelum mengembalikannya (source="database").
    """
    r = get_redis_client()

    cache_key = f"item:{item_id}"
    cached = r.get(cache_key)
    if cached is not None:
        data = json.loads(cached)
        return ItemResponse(**data, source="cache")

    # Jika tidak ada di cache, baca dari PostgreSQL
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, description FROM items WHERE id = %s",
                    (item_id,),
                )
                row = cur.fetchone()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = {"id": row[0], "name": row[1], "description": row[2]}

    # Simpan ke cache untuk permintaan berikutnya (misalnya selama 60 detik)
    r.setex(cache_key, 60, json.dumps(item_data))

    return ItemResponse(**item_data, source="database")


@app.get("/")
def root():
    """Endpoint sederhana untuk mengecek bahwa service berjalan."""
    return {
        "message": "Q1 CAP/BASE example API is running",
        "endpoints": [
            "/items/{item_id}  # GET: membaca item dengan pola cache-aside",
        ],
    }
