from sqlalchemy.orm import Session
from app.models import Category, MenuItem, Restaurant
from decimal import Decimal

def init_db(db: Session) -> None:
    categories_data = [
        {"name": "Шаурма", "description": "Вкуснейшая шаурма"},
        {"name": "Напитки", "description": "Освежающие напитки"},
        {"name": "Закуски", "description": "Вкусные закуски"},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not category:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
            db.refresh(category)
        categories[cat_data["name"]] = category
    
    menu_items = [
        {
            "name": "Шаурма за 5 рублей",
            "description": "Акционное предложение! Классическая шаурма по специальной цене",
            "price": Decimal("5.00"),
            "category_id": categories["Шаурма"].id,
            "image_url": "/images/shawarma-5.jpg"
        },
        {
            "name": "Шаурма с курицей",
            "description": "Сочная куриная шаурма с овощами и соусом",
            "price": Decimal("120.00"),
            "category_id": categories["Шаурма"].id,
            "image_url": "/images/shawarma-chicken.jpg"
        },
        {
            "name": "Шаурма с говядиной",
            "description": "Сытная шаурма с говядиной",
            "price": Decimal("150.00"),
            "category_id": categories["Шаурма"].id,
            "image_url": "/images/shawarma-beef.jpg"
        },
        {
            "name": "Шаурма вегетарианская",
            "description": "Шаурма с овощами и фалафелем",
            "price": Decimal("110.00"),
            "category_id": categories["Шаурма"].id,
            "image_url": "/images/shawarma-veg.jpg"
        },
        {
            "name": "Кола 0.5л",
            "description": "Coca-Cola 0.5л",
            "price": Decimal("70.00"),
            "category_id": categories["Напитки"].id,
            "image_url": "/images/cola.jpg"
        },
        {
            "name": "Вода 0.5л",
            "description": "Минеральная вода без газа",
            "price": Decimal("40.00"),
            "category_id": categories["Напитки"].id,
            "image_url": "/images/water.jpg"
        },
        {
            "name": "Чай",
            "description": "Горячий черный чай",
            "price": Decimal("50.00"),
            "category_id": categories["Напитки"].id,
            "image_url": "/images/tea.jpg"
        },
        {
            "name": "Картофель фри",
            "description": "Хрустящий картофель фри",
            "price": Decimal("90.00"),
            "category_id": categories["Закуски"].id,
            "image_url": "/images/fries.jpg"
        },
        {
            "name": "Наггетсы 6 шт",
            "description": "Куриные наггетсы",
            "price": Decimal("120.00"),
            "category_id": categories["Закуски"].id,
            "image_url": "/images/nuggets.jpg"
        },
        {
            "name": "Салат овощной",
            "description": "Свежий салат из овощей",
            "price": Decimal("80.00"),
            "category_id": categories["Закуски"].id,
            "image_url": "/images/salad.jpg"
        },
    ]
    
    for item_data in menu_items:
        existing = db.query(MenuItem).filter(MenuItem.name == item_data["name"]).first()
        if not existing:
            item = MenuItem(**item_data)
            db.add(item)
    
    db.commit()
    
    restaurants_data = [
        {
            "name": "Махачкала на ул. Ленина",
            "address": "ул. Ленина, д. 10",
            "latitude": 53.9045,
            "longitude": 27.5615,
            "phone": "+375291234567",
            "working_hours": {"mon-sun": "10:00-23:00"}
        },
        {
            "name": "Махачкала на пр. Независимости",
            "address": "пр. Независимости, д. 45",
            "latitude": 53.9168,
            "longitude": 27.5918,
            "phone": "+375291234568",
            "working_hours": {"mon-sun": "10:00-23:00"}
        },
        {
            "name": "Махачкала на ул. Кирова",
            "address": "ул. Кирова, д. 23",
            "latitude": 53.8900,
            "longitude": 27.5500,
            "phone": "+375291234569",
            "working_hours": {"mon-sun": "10:00-23:00"}
        },
    ]
    
    for rest_data in restaurants_data:
        existing = db.query(Restaurant).filter(Restaurant.name == rest_data["name"]).first()
        if not existing:
            restaurant = Restaurant(**rest_data)
            db.add(restaurant)
    
    db.commit()
    print("✅ Database initialized with seed data!")




