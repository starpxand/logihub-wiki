# Схема базы данных

Основные сущности предметной области: **Клиент, Заказ, Груз, Маршрут, Транспорт,
Водитель, Склад**.

<span id="er-diagram"></span>

```mermaid
erDiagram
    CLIENT ||--o{ ORDER : "оформляет"
    ORDER ||--|{ CARGO : "содержит"
    WAREHOUSE ||--o{ CARGO : "хранит"
    ORDER ||--o| ROUTE : "исполняется по"
    ROUTE }o--|| VEHICLE : "назначен"
    ROUTE }o--|| DRIVER : "выполняет"
    ROUTE ||--|{ ROUTE_POINT : "включает"

    CLIENT {
        uuid id PK
        string name
        string inn
        string contact_phone
        string telegram_id
    }
    ORDER {
        uuid id PK
        string number
        uuid client_id FK
        string status
        date planned_delivery
        date actual_delivery
        decimal price
        bool on_time
        bool in_full
    }
    CARGO {
        uuid id PK
        uuid order_id FK
        uuid warehouse_id FK
        string cargo_type
        decimal weight_kg
        decimal volume_m3
        string temp_mode
        string barcode
    }
    ROUTE {
        uuid id PK
        uuid order_id FK
        uuid vehicle_id FK
        uuid driver_id FK
        int distance_km
        timestamp eta
    }
    ROUTE_POINT {
        uuid id PK
        uuid route_id FK
        int seq
        string address
        timestamp arrived_at
    }
    VEHICLE {
        uuid id PK
        string plate
        string type
        int capacity_kg
        bool refrigerated
    }
    DRIVER {
        uuid id PK
        string full_name
        string license
        string phone
    }
    WAREHOUSE {
        uuid id PK
        string name
        string address
        int capacity_pallets
    }
```

## Описание сущностей

| Сущность | Назначение | Ключевые ограничения |
|---|---|---|
| Клиент | Грузоотправитель, заключивший договор | ИНН уникален |
| Заказ | Заявка на перевозку и её жизненный цикл | Статусы: `new → confirmed → paid → packed → in_transit → delivered → closed` |
| Груз | Грузовое место заказа | Штрихкод уникален; вес > 0 |
| Маршрут | План перевозки заказа | Вес груза ≤ грузоподъёмности ТС |
| Транспорт | Транспортное средство парка | Госномер уникален |
| Водитель | Исполнитель перевозки | Не более одного активного маршрута |
| Склад | Место хранения и комплектации | Вместимость в паллетах |
