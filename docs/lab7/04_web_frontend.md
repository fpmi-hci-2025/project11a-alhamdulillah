# Реализация Web Frontend

## 1. Структура проекта

```
makhachkala-web/
├── src/
│   ├── components/      # React компоненты
│   │   ├── Header/
│   │   ├── Footer/
│   │   ├── MenuCard/
│   │   └── Cart/
│   ├── pages/          # Страницы
│   │   ├── Home/
│   │   ├── Menu/
│   │   ├── Checkout/
│   │   └── Profile/
│   ├── store/          # Redux store
│   ├── services/       # API клиент
│   ├── styles/         # LESS/SCSS
│   ├── utils/          # Утилиты
│   └── App.jsx
├── public/
├── package.json
└── vite.config.js
```

## 2. Технологии

- **React** 18+
- **Vite** - build tool
- **React Router** - навигация
- **Redux Toolkit** - state management
- **Axios** - HTTP клиент
- **Bootstrap 5** + **LESS** - стилизация
- **React Hook Form** - работа с формами

## 3. Главная страница (Home)

### Компонент

```jsx
// src/pages/Home/Home.jsx
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPromoItems } from '../../store/menuSlice';
import MenuCard from '../../components/MenuCard/MenuCard';
import './Home.less';

export default function Home() {
  const dispatch = useDispatch();
  const { promoItems, loading } = useSelector(state => state.menu);
  
  useEffect(() => {
    dispatch(fetchPromoItems());
  }, [dispatch]);
  
  if (loading) return <div className="spinner">Загрузка...</div>;
  
  return (
    <div className="home-page">
      <section className="hero">
        <div className="container">
          <h1>Шаурма за 5 рублей!</h1>
          <p>Лучшая шаурма в городе по невероятной цене</p>
          <button className="btn btn-primary btn-lg">
            Заказать сейчас
          </button>
        </div>
      </section>
      
      <section className="promo-items">
        <div className="container">
          <h2>Акционные предложения</h2>
          <div className="row">
            {promoItems.map(item => (
              <div key={item.id} className="col-md-4">
                <MenuCard item={item} />
              </div>
            ))}
          </div>
        </div>
      </section>
      
      <section className="restaurants">
        <div className="container">
          <h2>Найти ближайший ресторан</h2>
          <button className="btn btn-outline-primary">
            Показать на карте
          </button>
        </div>
      </section>
    </div>
  );
}
```

### Стили (LESS)

```less
// src/pages/Home/Home.less
@import '../../styles/variables.less';

.home-page {
  .hero {
    background: linear-gradient(135deg, @brand-red, @brand-orange);
    color: white;
    padding: 80px 0;
    text-align: center;
    
    h1 {
      font-size: 3rem;
      font-weight: bold;
      margin-bottom: 20px;
    }
    
    p {
      font-size: 1.5rem;
      margin-bottom: 30px;
    }
  }
  
  .promo-items {
    padding: 60px 0;
    
    h2 {
      text-align: center;
      margin-bottom: 40px;
    }
  }
  
  .restaurants {
    background: @gray-light;
    padding: 60px 0;
    text-align: center;
  }
}
```

## 4. Страница меню (Menu)

### Компонент с фильтрами

```jsx
// src/pages/Menu/Menu.jsx
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMenuItems } from '../../store/menuSlice';
import MenuCard from '../../components/MenuCard/MenuCard';
import './Menu.less';

export default function Menu() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector(state => state.menu);
  const [filters, setFilters] = useState({
    category: '',
    search: ''
  });
  
  useEffect(() => {
    dispatch(fetchMenuItems(filters));
  }, [dispatch, filters]);
  
  const categories = ['SHAWARMA', 'DRINKS', 'SNACKS', 'DESSERTS'];
  
  return (
    <div className="menu-page">
      <div className="container">
        <h1>Наше меню</h1>
        
        <div className="filters">
          <input
            type="text"
            placeholder="Поиск блюд..."
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            className="form-control"
          />
          
          <div className="category-filters">
            <button 
              className={!filters.category ? 'active' : ''}
              onClick={() => setFilters({...filters, category: ''})}
            >
              Все
            </button>
            {categories.map(cat => (
              <button
                key={cat}
                className={filters.category === cat ? 'active' : ''}
                onClick={() => setFilters({...filters, category: cat})}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
        
        <div className="menu-grid">
          {loading ? (
            <div className="spinner">Загрузка...</div>
          ) : (
            items.map(item => (
              <MenuCard key={item.id} item={item} />
            ))
          )}
        </div>
      </div>
    </div>
  );
}
```

### MenuCard Component

```jsx
// src/components/MenuCard/MenuCard.jsx
import { useDispatch } from 'react-redux';
import { addToCart } from '../../store/cartSlice';
import './MenuCard.less';

export default function MenuCard({ item }) {
  const dispatch = useDispatch();
  
  const handleAddToCart = () => {
    dispatch(addToCart(item));
  };
  
  return (
    <div className="menu-card">
      <img src={item.imageUrl} alt={item.name} />
      <div className="card-body">
        <h3>{item.name}</h3>
        <p>{item.description}</p>
        <div className="price">
          {item.isPromo && item.promoPrice && (
            <span className="old-price">{item.price} ₽</span>
          )}
          <span className="current-price">
            {item.isPromo ? item.promoPrice : item.price} ₽
          </span>
        </div>
        <button 
          className="btn btn-primary"
          onClick={handleAddToCart}
        >
          В корзину
        </button>
      </div>
    </div>
  );
}
```

## 5. Redux Store

### Menu Slice

```javascript
// src/store/menuSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../services/api';

export const fetchMenuItems = createAsyncThunk(
  'menu/fetchItems',
  async (filters) => {
    const response = await api.get('/menu-items', { params: filters });
    return response.data.data;
  }
);

const menuSlice = createSlice({
  name: 'menu',
  initialState: {
    items: [],
    promoItems: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMenuItems.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchMenuItems.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchMenuItems.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default menuSlice.reducer;
```

### Cart Slice

```javascript
// src/store/cartSlice.js
import { createSlice } from '@reduxjs/toolkit';

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    totalPrice: 0
  },
  reducers: {
    addToCart: (state, action) => {
      const existingItem = state.items.find(
        item => item.id === action.payload.id
      );
      
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
      
      state.totalPrice = state.items.reduce((sum, item) => 
        sum + (item.isPromo ? item.promoPrice : item.price) * item.quantity, 
        0
      );
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter(item => item.id !== action.payload);
      state.totalPrice = state.items.reduce((sum, item) => 
        sum + (item.isPromo ? item.promoPrice : item.price) * item.quantity, 
        0
      );
    }
  }
});

export const { addToCart, removeFromCart } = cartSlice.actions;
export default cartSlice.reducer;
```

## 6. API Client

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api/v1',
  timeout: 10000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

## 7. Build и Deployment

### Vite Config

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
});
```

### Build Commands

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx",
    "test": "vitest"
  }
}
```

## 8. Оптимизация

### Lazy Loading

```jsx
// src/App.jsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home/Home'));
const Menu = lazy(() => import('./pages/Menu/Menu'));
const Checkout = lazy(() => import('./pages/Checkout/Checkout'));

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Загрузка...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu" element={<Menu />} />
          <Route path="/checkout" element={<Checkout />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

## Ссылки

- [Mobile реализация](05_mobile_implementation.md)
- [Макеты Lab5](../design/lab5/colors_compare.md)
- [Рекомендации Lab6](../lab6/10_recommendations.md)

