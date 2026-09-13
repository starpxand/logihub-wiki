<div align="center">

# 🚚 ЛогиХаб Wiki

**База знаний цифрового продукта «ЛогиХаб» – платформы управления процессом логистики**

*Каждая поставка – под контролем, в одном окне.*

[![Docs](https://img.shields.io/badge/docs-MkDocs%20Material-283593?logo=materialformkdocs&logoColor=white)](https://starpxand.github.io/logihub-wiki/)
[![Deploy](https://github.com/starpxand/logihub-wiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/starpxand/logihub-wiki/actions/workflows/deploy.yml)
![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Открыть Wiki](https://starpxand.github.io/logihub-wiki/) ·
[Дашборд](https://github.com/starpxand/logihub-dashboard) ·
[Telegram-бот](https://github.com/starpxand/logihub-telegram-bot)

</div>

---

## О проекте

Wiki документирует учебный цифровой продукт **«ЛогиХаб»** (вариант 15 «Процесс
управления логистикой») и состоит из двух частей:

| Часть | Содержание |
|---|---|
| **Продуктовая** | Определение продукта и слоган, главный KPI (OTIF) с историей релизов, развитие продукта, артефакты, таблица ролей |
| **Техническая** | Требования, архитектура микросервисов, схема БД, API, тестирование, безопасность, развёртывание |
| **Процессы** | BPMN 2.0-модель процесса управления логистикой |
| **Команда** | Регламент дежурств, применение ИИ, журнал изменений |

## Структура репозитория

```text
logihub-wiki/
├── docs/                   # страницы Wiki (Markdown)
│   ├── product/            # продуктовая часть
│   ├── tech/               # техническая часть
│   ├── process/            # BPMN-модели
│   ├── team/               # регламенты команды
│   └── assets/             # графики, изображения, стили
├── scripts/build_charts.py # построение графиков KPI из выгрузки заказов
├── mkdocs.yml              # конфигурация сайта
└── requirements.txt
```

## Локальный запуск

```bash
git clone https://github.com/starpxand/logihub-wiki.git
cd logihub-wiki
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
```

Пересборка графиков KPI из данных дашборда:

```bash
python scripts/build_charts.py ../logihub-dashboard/data/logistics_orders.csv
```

## Публикация

Сайт публикуется на **GitHub Pages** автоматически workflow
[`deploy.yml`](.github/workflows/deploy.yml) при каждом push в ветку `main`.

## Как предложить правку

1. Создайте ветку `docs/<кратко-о-правке>`.
2. Отредактируйте Markdown-страницы в `docs/`, проверьте `mkdocs build --strict`.
3. Откройте Pull Request и добавьте запись в `docs/team/changelog.md`.

## Автор

**Попов А.С.**, группа 5ИТб-2, ФГБОУ ВО «КнАГУ» · GitHub: [@starpxand](https://github.com/starpxand)

Лицензия – [MIT](LICENSE).
