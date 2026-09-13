# API

Все запросы проходят через API Gateway `https://api.logihub.example/v1`.
Формат – JSON, аутентификация – `Authorization: Bearer <JWT>`.

| Метод | Путь | Сервис | Назначение |
|---|---|---|---|
| `POST` | `/orders` | Заказы | Создать заявку на перевозку |
| `GET` | `/orders/{id}` | Заказы | Карточка заказа и текущий статус |
| `POST` | `/orders/{id}/quote` | Заказы | Расчёт стоимости и срока доставки |
| `POST` | `/orders/{id}/confirm` | Заказы | Подтверждение клиентом |
| `POST` | `/warehouse/picks` | Склад | Создать задание на комплектацию |
| `POST` | `/warehouse/picks/{id}/scan` | Склад | Сканирование маркировки грузового места |
| `POST` | `/routes/plan` | Маршрутизация | Построить маршрут и подобрать ТС |
| `GET` | `/tracking/{order_id}` | Трекинг | Геопозиция, ETA, история статусов |
| `POST` | `/tracking/{order_id}/events` | Трекинг | Событие водителя (погрузка, выгрузка, инцидент) |
| `GET` | `/analytics/otif?from=&to=` | Заказы | OTIF за период |

## Пример: создание заявки

```http
POST /v1/orders
Content-Type: application/json

{
  "client_id": "7b1c…",
  "origin": "Комсомольск-на-Амуре, ул. Заводская, 1",
  "destination": "Хабаровск, ул. Промышленная, 12",
  "cargo": [{"type": "Продукты питания", "weight_kg": 3200, "temp_mode": "+2..+6"}],
  "desired_date": "2026-09-20"
}
```

```json
{"id": "LH-15872", "status": "new", "price_estimate": 48750.00, "eta": "2026-09-21"}
```
