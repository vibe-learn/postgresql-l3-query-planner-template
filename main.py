"""Homework scaffold — postgresql lesson `l3_query_planner` (Vibe Learn).

Задача: pg_stat_statements: топ-10 по total_exec_time, EXPLAIN ANALYZE топ-3 и рекомендации.

Реализуй функции ниже — сигнатуры и тестовая поверхность фиксированы;
CI (.github/workflows/ci.yml) ставит зависимости и гоняет `pytest`.
Подробности и критерии приёмки — в README.md.

Драйвер: psycopg (v3). DSN берётся из env DATABASE_URL.
"""

import os

import psycopg


def database_url() -> str:
    """DSN PostgreSQL из env. Дефолт совпадает с docker-compose.yml."""
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/postgres",
    )


def connect() -> "psycopg.Connection":
    """Открыть соединение psycopg из DATABASE_URL."""
    return psycopg.connect(database_url())


# ----- TODO #1: top_statements -----
def top_statements(conn, n: int = 10) -> list[dict]:
    """SELECT query, total_exec_time, calls FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT n"""
    raise NotImplementedError("top_statements: реализуй меня")


# ----- TODO #2: explain_json -----
def explain_json(conn, sql: str, params: tuple = ()) -> dict:
    """EXPLAIN (ANALYZE, FORMAT JSON) → dict дерева плана"""
    raise NotImplementedError("explain_json: реализуй меня")


# ----- TODO #3: recommend -----
def recommend(plan: dict) -> list[str]:
    """чистая функция: пройти по плану, выдать флаги «Seq Scan на >100k строк», «estimate vs actual >10×»"""
    raise NotImplementedError("recommend: реализуй меня")



def main() -> None:
    """Точка входа: подключиться и напомнить, что реализовать.

    Замени тело на демонстрацию реализованных функций.
    """
    print("Vibe Learn — postgresql lesson scaffold up")
    print(f"DATABASE_URL: {database_url()}")
    print("Реализуй TODO-функции, затем `pytest`. README.md содержит задачу.")


if __name__ == "__main__":
    main()
