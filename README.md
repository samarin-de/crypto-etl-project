# Crypto ETL Pipeline

Автоматизированный ETL-пайплайн для сбора и хранения курсов криптовалют с использованием Airflow, Docker, PostgreSQL и Python.

## О проекте

Проект собирает актуальные курсы Bitcoin (BTC) и Ethereum (ETH) с публичного API CoinGecko, сохраняет их в PostgreSQL и управляется через Apache Airflow.

Этот пайплайн демонстрирует:
- Оркестрацию задач через Airflow
- Работу с внешними API
- Контейнеризацию с Docker и Docker Compose
- Интеграцию Python с PostgreSQL
- Обработку ошибок и логирование
- Передачу данных между задачами (XCom)

## Архитектура

CoinGecko API (REST)
        │
        ▼
┌───────────────────┐
│  fetch_prices.py  │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│    PostgreSQL     │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Airflow DAG      │
└───────────────────┘


## Стек технологий

- Python 3.11  основной язык скрипта
- PostgreSQL  хранение исторических данных
- Apache Airflow  оркестрация и планирование
- Docker / Docker Compose  контейнеризация
- Git / GitHub  контроль версий
- CoinGecko API  источник данных

## Запуск проекта

1. Клонировать репозиторий:
   git clone https://github.com/samarin-de/crypto-etl-project.git
   cd crypto-etl-project

2. Собрать и запустить через Docker Compose:
   docker-compose up --build

3. Запустить ETL-скрипт вручную:
   docker-compose run --rm crypto-etl

4. Запустить через Airflow (по расписанию):
   Проект интегрирован с Airflow через DAG crypto_etl_dag.
   Airflow запускает контейнер автоматически каждые 10 минут.

## Проверка данных в PostgreSQL

docker exec -it crypto_postgres psql -U crypto_user -d crypto_db -c "SELECT * FROM crypto_prices ORDER BY id DESC LIMIT 5;"

## Структура проекта

crypto-etl-project/
 fetch_prices.py          # Основной ETL-скрипт
 Dockerfile               # Сборка образа для ETL
 docker-compose.yml       # Оркестрация контейнеров
 .gitignore               # Игнорируемые файлы
 README.md                # Описание проекта

## Пример результата в XCom (Airflow)

return_value: [2026-07-11 12:42:02] BTC: 64088 USD, ETH: 1797.35 USD

## Что дальше

- Добавить Telegram-уведомления
- Добавить агрегацию через Apache Spark
- Развернуть в облаке (Yandex Cloud / AWS)

## Контакты

Автор: Sergey Samarin
GitHub: samarin-de
Проект: https://github.com/samarin-de/crypto-etl-project

## Лицензия

Этот проект создан в учебных целях.
