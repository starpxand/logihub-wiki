---
template: home.html
title: Главная
hide:
  - navigation
  - toc
---

# База знаний продукта

Wiki – единая точка правды для команды ЛогиХаба. Выберите раздел, чтобы начать.

<div class="grid cards" markdown>

-   :material-bullseye-arrow:{ .lg .middle } **Определение продукта**

    ---

    Какую проблему решаем, для кого делаем продукт и чем он отличается.

    [:octicons-arrow-right-24: Открыть](product/definition.md)

-   :material-chart-timeline-variant-shimmer:{ .lg .middle } **Состояние продукта**

    ---

    Главный KPI – OTIF – и его динамика по релизам v1.0 → v1.5 → v2.0.

    [:octicons-arrow-right-24: KPI и графики](product/state.md)

-   :material-map-marker-path:{ .lg .middle } **Развитие продукта**

    ---

    Цели, эпики, гипотезы, дорожная карта, очереди и доска спринта.

    [:octicons-arrow-right-24: Дорожная карта](product/roadmap.md)

-   :material-folder-star-outline:{ .lg .middle } **Артефакты**

    ---

    Интервью с клиентами, exit-интервью, схемы и дизайн-документы.

    [:octicons-arrow-right-24: Материалы](product/artifacts.md)

-   :material-sitemap-outline:{ .lg .middle } **Архитектура**

    ---

    Микросервисы «Заказы», «Склад», «Маршрутизация», «Трекинг», «Уведомления».

    [:octicons-arrow-right-24: Техническая часть](tech/architecture.md)

-   :material-account-group-outline:{ .lg .middle } **Команда и роли**

    ---

    Зоны ответственности, матрица RACI и регламент дежурств.

    [:octicons-arrow-right-24: Таблица ролей](product/roles.md)

</div>

## Быстрые ссылки

| Ресурс | Где находится |
|---|---|
| Продуктовая очередь (бэклог) | [GitHub Issues · label `product`](https://github.com/starpxand/logihub-wiki/issues?q=label%3Aproduct) |
| Техническая очередь | [GitHub Issues · label `tech-debt`](https://github.com/starpxand/logihub-wiki/issues?q=label%3Atech-debt) |
| Доска спринта | [GitHub Projects · «ЛогиХаб – Спринт»](https://github.com/users/starpxand/projects) |
| Расписание дежурств | [Регламент дежурств](team/on-call.md) |
| Исходный код Wiki | [starpxand/logihub-wiki](https://github.com/starpxand/logihub-wiki) |

!!! info "Как вносить изменения"
    Wiki ведётся по принципу «docs as code»: правки – через Pull Request в
    репозиторий, публикация на GitHub Pages – автоматически после слияния в `main`.
