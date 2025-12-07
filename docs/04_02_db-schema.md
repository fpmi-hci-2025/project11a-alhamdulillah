---
layout: page
title: Схема базы данных
permalink: /db-schema
---

# Логическая Схема базы данных

| Сущность        | Атрибут                | Тип данных / Описание                                   | Обязательно | 
|-----------------|------------------------|----------------------------------------------------------|-------------|
| **Пользователь** (users) | id                     | INT, первичный ключ                                     | Да          |
|                 | role                   | VARCHAR(20) — роль (client, admin, courier)             | Да          |
|                 | name                   | VARCHAR(100) — имя пользователя                         | Да          |
|                 | phone                  | VARCHAR(20) — телефон (уникальный)                      | Да          |
|                 | email                  | VARCHAR(100) — email (уникальный)                       | Нет         |
|                 | password_hash          | VARCHAR(255) — хэш пароля                               | Да          |
|                 | created_at             | DATETIME — дата регистрации                             | Да          |
| **Ресторан** (restaurants) | id              | INT, первичный ключ                                     | Да          |
|                 | name                   | VARCHAR(100) — название точки                           | Да          |
|                 | address                | TEXT — полный адрес                                     | Да          |
|                 | latitude               | DECIMAL(10,8) — широта                                  | Нет         |
|                 | longitude              | DECIMAL(11,8) — долгота                                 | Нет         |
|                 | schedule               | VARCHAR(255) — график работы                            | Нет         |
|                 | status                 | VARCHAR(20) — статус (open/closed)                      | Да          |
| **Акция** (promotions) | id               | INT, первичный ключ                                     | Да          |
|                 | title                  | VARCHAR(255) — название акции                           | Да          |
|                 | description            | TEXT — описание                                         | Нет         |
|                 | condition              | TEXT — условие акции                                    | Нет         |
|                 | start_date             | DATE — дата начала                                      | Да          |
|                 | end_date               | DATE — дата окончания                                   | Да          |
| **Блюдо** (dishes) | id               | INT, первичный ключ                                     | Да          |
|                 | name                   | VARCHAR(255) — название блюда                           | Да          |
|                 | description            | TEXT — описание                                         | Нет         |
|                 | price                  | DECIMAL(10,2) — цена в рублях                           | Да          |
|                 | category               | VARCHAR(50) — категория                                 | Нет         | 
|                 | image_url              | VARCHAR(500) — ссылка на фото                           | Нет         |
|                 | restaurant_id          | INT, внешний ключ → restaurants.id                      | Да          |
|                 | promotion_id           | INT, внешний ключ → promotions.id                       | Нет         |
| **Заказ** (orders) | id               | INT, первичный ключ                                     | Да          | 
|                 | user_id                | INT, внешний ключ → users.id                            | Да          |
|                 | restaurant_id          | INT, внешний ключ → restaurants.id                      | Да          |
|                 | status                 | VARCHAR(30) — статус заказа                             | Да          |
|                 | payment_method         | VARCHAR(30) — способ оплаты                             | Нет         |
|                 | total_amount           | DECIMAL(10,2) — общая сумма                             | Да          |
|                 | delivery_address       | TEXT — адрес доставки                                   | Нет         |
|                 | created_at             | DATETIME — время создания                               | Да          |
|                 | completed_at           | DATETIME — время завершения                             | Нет         |
| **Позиция заказа** (order_items) | id        | INT, первичный ключ                                     | Да          |
|                 | order_id               | INT, внешний ключ → orders.id                           | Да          |
|                 | dish_id                | INT, внешний ключ → dishes.id                           | Да          |
|                 | quantity               | INT — количество                                        | Да          |
|                 | price_at_order         | DECIMAL(10,2) — цена на момент заказа                   | Да          |

---

**Связи между сущностями:**

1. **Пользователь → Заказ** (1:N)  
   Один пользователь может создавать много заказов.

2. **Ресторан → Блюдо** (1:N)  
   В одном ресторане может быть много блюд.

3. **Акция → Блюдо** (1:N)  
   Одна акция может применяться к нескольким блюдам.

4. **Заказ → Позиция заказа** (1:N)  
   Один заказ может содержать несколько позиций.

5. **Блюдо → Позиция заказа** (1:N)  
   Одно блюдо может входить в разные позиции заказов.

6. **Ресторан → Заказ** (1:N)  
   Один ресторан может выполнять много заказов.

# Физическая модель (ER-диаграмма)

[ER-диаграмма БД](https://tinyurl.com/27q576qm)<!--[ER-диаграмма БД](./diagrams/puml/04_02_erd_diagram_physical.puml)-->

# SQL-файл

Полный SQL для создания базы данных доступен здесь: [db-schema.sql](/project11a-alhamdulillah/blob/main/docs/04_02_db-schema.sql)