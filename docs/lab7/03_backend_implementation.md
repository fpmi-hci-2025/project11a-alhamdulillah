# Реализация Backend

## 1. Структура проекта

```
makhachkala-backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── menu.py
│   │   │   ├── orders.py
│   │   │   ├── auth.py
│   │   │   └── restaurants.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   ├── menu_item.py
│   │   ├── order.py
│   │   └── restaurant.py
│   ├── schemas/
│   │   ├── menu.py
│   │   ├── order.py
│   │   └── user.py
│   ├── crud/
│   │   ├── menu.py
│   │   └── order.py
│   └── main.py
├── tests/
├── alembic/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 2. Модели данных (SQLAlchemy)

### MenuItem Model

```python
from sqlalchemy import Column, String, Decimal, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Decimal(10, 2), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Order Model

```python
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"))
    total = Column(Decimal(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    delivery_type = Column(Enum(DeliveryType))
    address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
```

## 3. API Endpoints

### Menu API (`/api/menu`)

**GET /api/menu** - Список блюд
```python
@router.get("/menu", response_model=List[MenuItemResponse])
async def get_menu(
    category_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    items = crud.menu.get_items(
        db, 
        category_id=category_id, 
        skip=skip, 
        limit=limit
    )
    return items
```

**GET /api/menu/{id}** - Детали блюда
```python
@router.get("/menu/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    item_id: UUID,
    db: Session = Depends(get_db)
):
    item = crud.menu.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### Orders API (`/api/orders`)

**POST /api/orders** - Создать заказ
```python
@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = crud.order.create_with_user(
        db, 
        obj_in=order_in, 
        user_id=current_user.id
    )
    return order
```

**GET /api/orders** - Список заказов пользователя
```python
@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    orders = crud.order.get_by_user(
        db, 
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return orders
```

## 4. CRUD операции (пример для Menu)

```python
class CRUDMenuItem(CRUDBase[MenuItem, MenuItemCreate, MenuItemUpdate]):
    def get_items(
        self,
        db: Session,
        *,
        category_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MenuItem]:
        query = db.query(self.model).filter(
            self.model.is_available == True
        )
        
        if category_id:
            query = query.filter(self.model.category_id == category_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_category(
        self, 
        db: Session, 
        category_id: UUID
    ) -> List[MenuItem]:
        return db.query(self.model).filter(
            self.model.category_id == category_id,
            self.model.is_available == True
        ).all()

menu_item = CRUDMenuItem(MenuItem)
```

## 5. Схемы (Pydantic)

```python
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: UUID
    image_url: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: UUID
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 6. Seed данные

```python
def seed_menu(db: Session):
    categories = [
        Category(id=uuid.uuid4(), name="Шаурма"),
        Category(id=uuid.uuid4(), name="Напитки"),
        Category(id=uuid.uuid4(), name="Закуски"),
    ]
    
    menu_items = [
        MenuItem(
            name="Шаурма за 5 рублей",
            description="Акционное предложение!",
            price=5.00,
            category_id=categories[0].id,
            image_url="/images/shawarma-5.jpg"
        ),
        MenuItem(
            name="Шаурма с курицей",
            description="Классическая шаурма с курицей",
            price=120.00,
            category_id=categories[0].id,
            image_url="/images/shawarma-chicken.jpg"
        ),
        # ... больше блюд
    ]
    
    db.add_all(categories)
    db.add_all(menu_items)
    db.commit()
```

## 7. Тестирование

### Unit-тесты (pytest)

```python
def test_create_menu_item(db: Session):
    item_in = MenuItemCreate(
        name="Test Shawarma",
        description="Test",
        price=100.00,
        category_id=test_category_id
    )
    
    item = crud.menu_item.create(db, obj_in=item_in)
    
    assert item.name == "Test Shawarma"
    assert item.price == 100.00
    assert item.is_available == True

def test_get_menu_items(client: TestClient):
    response = client.get("/api/menu")
    
    assert response.status_code == 200
    assert len(response.json()) > 0
```

## 8. Docker настройка

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: makhachkala
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/makhachkala
    depends_on:
      - db

volumes:
  postgres_data:
```

## 9. Документация API (Swagger)

FastAPI автоматически генерирует документацию:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 10. Deployment

### Railway

```bash
# Установка Railway CLI
npm install -g @railway/cli

# Деплой
railway login
railway init
railway up
```

## Результаты Sprint 1

- ✅ Настроен проект FastAPI
- ✅ Созданы модели MenuItem, Category, Restaurant
- ✅ Реализованы CRUD операции для меню
- ✅ API endpoints для меню работают
- ✅ Seed данные добавлены
- ✅ Docker контейнеризация
- ✅ Базовые тесты написаны

## Ссылки

- [Техническое задание](01_technical_specification.md)
- [Frontend реализация](04_web_frontend.md)
- [API документация](http://localhost:8000/docs)
- [GitHub Repository](https://github.com/fpmi-hci-2025/makhachkala-backend)
