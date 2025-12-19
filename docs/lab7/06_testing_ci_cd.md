# Тестирование и CI/CD

## 1. GitHub Actions CI/CD

### Backend Pipeline

```yaml
# .github/workflows/backend.yml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Prisma migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
      
      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
```

### Frontend Pipeline

```yaml
# .github/workflows/frontend.yml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      
      - name: Deploy to Vercel
        if: github.ref == 'refs/heads/main'
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 2. Типы тестов

### Unit тесты (Jest)

```javascript
// tests/services/orderService.test.js
describe('OrderService', () => {
  describe('calculateTotalPrice', () => {
    it('should calculate correct price for regular items', () => {
      const items = [
        { price: 100, quantity: 2 },
        { price: 50, quantity: 1 }
      ];
      
      expect(calculateTotalPrice(items)).toBe(250);
    });
    
    it('should apply promo price when available', () => {
      const items = [
        { price: 100, promoPrice: 5, isPromo: true, quantity: 1 }
      ];
      
      expect(calculateTotalPrice(items)).toBe(5);
    });
  });
});
```

### Integration тесты

```javascript
// tests/integration/orders.test.js
describe('Orders API Integration', () => {
  let authToken;
  let userId;
  
  beforeAll(async () => {
    // Create test user and get token
    const user = await createTestUser();
    authToken = await loginUser(user);
    userId = user.id;
  });
  
  it('should create order with items', async () => {
    const orderData = {
      restaurantId: '...',
      deliveryType: 'DELIVERY',
      items: [
        { menuItemId: '...', quantity: 2 }
      ]
    };
    
    const res = await request(app)
      .post('/api/v1/orders')
      .set('Authorization', `Bearer ${authToken}`)
      .send(orderData)
      .expect(201);
    
    expect(res.body.success).toBe(true);
    expect(res.body.data.userId).toBe(userId);
  });
});
```

### E2E тесты (Cypress/Playwright)

```javascript
// e2e/order-flow.spec.js
describe('Order Flow', () => {
  it('should complete full order flow', () => {
    cy.visit('/');
    
    // Find promo shawarma
    cy.contains('Шаурма за 5 рублей').click();
    
    // Add to cart
    cy.contains('В корзину').click();
    
    // Go to checkout
    cy.get('[data-testid="cart-icon"]').click();
    cy.contains('Оформить заказ').click();
    
    // Fill form
    cy.get('[name="deliveryAddress"]').type('ул. Ленина, 10');
    cy.get('[name="deliveryType"]').select('DELIVERY');
    
    // Submit
    cy.contains('Подтвердить заказ').click();
    
    // Check success
    cy.contains('Заказ оформлен').should('be.visible');
  });
});
```

## 3. Code Quality Tools

### ESLint

```json
// .eslintrc.json
{
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "env": {
    "browser": true,
    "node": true,
    "es2021": true
  },
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error"
  }
}
```

### Prettier

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

## 4. Performance Testing

### Artillery Load Test

```yaml
# artillery-config.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"

scenarios:
  - name: "Get menu items"
    flow:
      - get:
          url: "/api/v1/menu-items"
```

**Запуск**: `artillery run artillery-config.yml`

## 5. Генератор тестовых данных (Mockaroo)

### API запрос

```javascript
// scripts/generateTestData.js
const axios = require('axios');

async function generateUsers(count = 100) {
  const response = await axios.post(
    'https://api.mockaroo.com/api/generate.json',
    {
      key: process.env.MOCKAROO_API_KEY,
      count,
      fields: [
        { name: 'firstName', type: 'First Name' },
        { name: 'lastName', type: 'Last Name' },
        { name: 'email', type: 'Email Address' },
        { name: 'phone', type: 'Phone', format: '+375 ## ### ## ##' }
      ]
    }
  );
  
  return response.data;
}
```

## 6. Monitoring и Logging

### Winston Logger

```javascript
// src/utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

module.exports = logger;
```

## 7. Postman коллекция

### Экспорт коллекции

```json
{
  "info": {
    "name": "Makhachkala API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\",\n  \"firstName\": \"Test\",\n  \"lastName\": \"User\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{baseUrl}}/auth/register"
          }
        }
      ]
    }
  ]
}
```

## 8. Coverage отчеты

### Jest Coverage

```json
{
  "jest": {
    "collectCoverage": true,
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

**Запуск**: `npm test -- --coverage`

## Ссылки

- [Backend реализация](03_backend_implementation.md)
- [Отчет о работах](07_work_report.md)
- [Техническое задание](01_technical_specification.md)

