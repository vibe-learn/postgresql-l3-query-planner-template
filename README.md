        # postgresql — Query planner, EXPLAIN ANALYZE и pg_stat_statements

        Homework-шаблон для урока **l3_query_planner** (Query planner, EXPLAIN ANALYZE и pg_stat_statements) на платформе Vibe Learn.

        ## Что делать

        Дано: testcontainers PG + база с users + orders (миллион строк). Реализуй Python-скрипт:
1) Поднять pg_stat_statements (через shared_preload_libraries в конфиге контейнера).
2) Сгенерировать 100 разных запросов с параметрами, выполнить.
3) Распарсить pg_stat_statements, вывести топ-10 по total_exec_time.
4) Для топ-3 — снять EXPLAIN ANALYZE (JSON формат) и распарсить дерево плана.
5) Сгенерировать рекомендации: «Seq Scan на > 100k строк», «estimate vs actual > 10×».
Тесты проверят корректность парсинга плана и фильтра top-by-time.

## Контекст (из transfer-задачи урока)

Производственный инцидент: на дашборде DBA замечает, что один из endpoint-ов API
деградировал с p95=80мс до p95=2.4с за последние сутки. Из логов pg_stat_statements
видно, что **один и тот же запрос** теперь тратит 2400мс на вызов (был 80мс):

```sql
SELECT u.email, count(o.id) AS orders_total, max(o.created_at) AS last_order_at
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.country = 'RU' AND u.created_at > now() - INTERVAL '180 days'
GROUP BY u.email;
```

## Recap из урока

- **Планировщик работает по статистике, не по гаданию.** Запускай `ANALYZE table;` после массовых изменений (COPY, миграции, bulk DELETE).
- **EXPLAIN ANALYZE — главный диагностический инструмент.** Без него оптимизация = угадывание. С BUFFERS видишь реальный I/O.
- **Главный red flag в плане:** rows estimate vs actual расходятся в N× раз — планировщик слепой, нужна свежая статистика.
- **pg_stat_statements — обязательное расширение в проде.** Топ-20 запросов по total_exec_time = твой план оптимизации на неделю.
- **SSD требует тюнинга random_page_cost.** Дефолт 4.0 — для HDD; ставь 1.1 для NVMe, иначе планировщик переоценивает Index Scan.

        ## Как работать

        1. Платформа Vibe Learn создаёт копию этого репо в твоём GitHub-аккаунте по клику «Начать домашку» на странице урока (через GitHub `/generate`, codecrafters-pattern).
        2. Склонируй копию локально, реализуй TODO в `main.py`, прогони тесты, запушь.
        3. CI (`.github/workflows/ci.yml`) ставит зависимости и запускает `pytest` на каждый push. Платформа слушает результат через webhook от GitHub Actions и обновляет статус домашки на странице урока.

        ## Локальное окружение

        - Python 3.12+
        - Docker + docker-compose — `docker compose up -d` поднимает single-node PostgreSQL 16 на `localhost:5432` с healthcheck. DSN: `postgresql://postgres:postgres@localhost:5432/postgres`. Переопределяется через env `DATABASE_URL`.

        ## Запуск

        ```bash
        # Поднять локальный PostgreSQL
        docker compose up -d

        # Установить зависимости
        pip install -r requirements.txt

        # Прогнать тесты (интеграционный включается через PG_INTEGRATION=1)
        pytest
        PG_INTEGRATION=1 pytest

        # Запустить main (печатает marker; замени stub на реализацию)
        python main.py
        ```

        ## Заметка автора

        Это baseline-шаблон, сгенерированный платформой. Бизнес-сущность задачи (что конкретно реализовать в `main.py`, какие тесты сделать строгими) расширяется по ходу итераций — параллельно с углублением теории урока.
