import asyncpg

from typing import Optional

class DAO:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.db_url)

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def add_user(self, tg_id:int, username:str, is_admin=False):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT OR IGNORE INTO
            """)


    # sql по которому созданы таблицы
    async def db_init(self):
        if not self.pool:
            self.pool = await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute("""  
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                tg_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                is_admin BOOLEAN DEFAULT FALSE
            );

            CREATE TABLE IF NOT EXISTS expense_categories (
                category_id SERIAL PRIMARY KEY,
                category_name TEXT UNIQUE NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            );

            CREATE TABLE IF NOT EXISTS income (
                income_id SERIAL PRIMARY KEY,
                amount DECIMAL(10,2) NOT NULL,
                comment_text TEXT,
                currency VARCHAR(3) NOT NULL DEFAULT 'BYN',
                datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS expense (
                expense_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                category_id INT NOT NULL REFERENCES expense_categories(category_id) ON DELETE RESTRICT,
                amount DECIMAL(10,2) NOT NULL,
                comment_text TEXT,
                date_time_expense TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                currency VARCHAR(3) DEFAULT 'BYN'
            );
            """)

            await conn.execute("""
                INSERT INTO expense_categories (category_name)
                VALUES ('Еда'), ('Декор'), ('Stuff')
                ON CONFLICT (category_name) DO NOTHING
            """
            )