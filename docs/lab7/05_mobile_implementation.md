# Реализация Mobile приложения

## 1. Технологии

- **React Native** 0.72+
- **React Navigation** - навигация
- **Redux Toolkit** - state management
- **Axios** - HTTP клиент
- **React Native Paper** - UI компоненты
- **AsyncStorage** - локальное хранилище

## 2. Структура проекта

```
makhachkala-mobile/
├── src/
│   ├── components/
│   ├── screens/
│   │   ├── HomeScreen/
│   │   ├── MenuScreen/
│   │   └── ProfileScreen/
│   ├── navigation/
│   ├── store/
│   ├── services/
│   └── theme/
├── android/
├── ios/
└── package.json
```

## 3. Навигация

```jsx
// src/navigation/AppNavigator.jsx
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Icon from 'react-native-vector-icons/MaterialIcons';

import HomeScreen from '../screens/HomeScreen';
import MenuScreen from '../screens/MenuScreen';
import OrdersScreen from '../screens/OrdersScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ color, size }) => {
          const icons = {
            Home: 'home',
            Menu: 'restaurant-menu',
            Orders: 'list-alt',
            Profile: 'person'
          };
          return <Icon name={icons[route.name]} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#e74c3c',
        tabBarInactiveTintColor: 'gray'
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: 'Главная' }} />
      <Tab.Screen name="Menu" component={MenuScreen} options={{ title: 'Меню' }} />
      <Tab.Screen name="Orders" component={OrdersScreen} options={{ title: 'Заказы' }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: 'Профиль' }} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Main" 
          component={MainTabs} 
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## 4. Главный экран

```jsx
// src/screens/HomeScreen/HomeScreen.jsx
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPromoItems } from '../../store/menuSlice';

export default function HomeScreen({ navigation }) {
  const dispatch = useDispatch();
  const { promoItems, loading } = useSelector(state => state.menu);
  
  useEffect(() => {
    dispatch(fetchPromoItems());
  }, []);
  
  return (
    <ScrollView style={styles.container}>
      {/* Hero Banner */}
      <View style={styles.hero}>
        <Image 
          source={require('../../assets/hero-bg.jpg')} 
          style={styles.heroImage}
        />
        <View style={styles.heroOverlay}>
          <Text style={styles.heroTitle}>Шаурма за 5 рублей!</Text>
          <Text style={styles.heroSubtitle}>Акция дня</Text>
          <TouchableOpacity 
            style={styles.heroButton}
            onPress={() => navigation.navigate('Menu')}
          >
            <Text style={styles.heroButtonText}>Заказать</Text>
          </TouchableOpacity>
        </View>
      </View>
      
      {/* Promo Items */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Акции</Text>
        {promoItems.map(item => (
          <TouchableOpacity 
            key={item.id} 
            style={styles.promoCard}
            onPress={() => navigation.navigate('Menu', { itemId: item.id })}
          >
            <Image source={{ uri: item.imageUrl }} style={styles.promoImage} />
            <View style={styles.promoInfo}>
              <Text style={styles.promoName}>{item.name}</Text>
              <Text style={styles.promoPrice}>{item.promoPrice} ₽</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>
      
      {/* Quick Actions */}
      <View style={styles.section}>
        <TouchableOpacity 
          style={styles.quickAction}
          onPress={() => navigation.navigate('Restaurants')}
        >
          <Icon name="location-on" size={24} color="#e74c3c" />
          <Text style={styles.quickActionText}>Найти ресторан</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff'
  },
  hero: {
    height: 250,
    position: 'relative'
  },
  heroImage: {
    width: '100%',
    height: '100%'
  },
  heroOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.4)',
    justifyContent: 'center',
    alignItems: 'center'
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10
  },
  heroSubtitle: {
    fontSize: 18,
    color: '#fff',
    marginBottom: 20
  },
  heroButton: {
    backgroundColor: '#e74c3c',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 25
  },
  heroButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  },
  section: {
    padding: 15
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 15
  },
  promoCard: {
    flexDirection: 'row',
    backgroundColor: '#f8f9fa',
    borderRadius: 10,
    marginBottom: 10,
    overflow: 'hidden'
  },
  promoImage: {
    width: 100,
    height: 100
  },
  promoInfo: {
    flex: 1,
    padding: 15,
    justifyContent: 'center'
  },
  promoName: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5
  },
  promoPrice: {
    fontSize: 20,
    color: '#e74c3c',
    fontWeight: 'bold'
  },
  quickAction: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 10
  },
  quickActionText: {
    marginLeft: 10,
    fontSize: 16,
    fontWeight: '500'
  }
});
```

## 5. Экран меню со свайпами

```jsx
// src/screens/MenuScreen/MenuScreen.jsx
import { View, FlatList, StyleSheet } from 'react-native';
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMenuItems } from '../../store/menuSlice';
import { addToCart } from '../../store/cartSlice';
import Swipeable from 'react-native-gesture-handler/Swipeable';
import MenuCard from '../../components/MenuCard';

export default function MenuScreen() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector(state => state.menu);
  const [filters, setFilters] = useState({ category: '', search: '' });
  
  useEffect(() => {
    dispatch(fetchMenuItems(filters));
  }, [filters]);
  
  const handleSwipeLeft = (item) => {
    dispatch(addToCart(item));
    // Показать уведомление
  };
  
  const renderRightActions = () => (
    <View style={styles.swipeAction}>
      <Text style={styles.swipeActionText}>В корзину</Text>
    </View>
  );
  
  const renderItem = ({ item }) => (
    <Swipeable
      renderRightActions={renderRightActions}
      onSwipeableRightOpen={() => handleSwipeLeft(item)}
    >
      <MenuCard item={item} />
    </Swipeable>
  );
  
  return (
    <View style={styles.container}>
      <FlatList
        data={items}
        renderItem={renderItem}
        keyExtractor={item => item.id}
        refreshing={loading}
        onRefresh={() => dispatch(fetchMenuItems(filters))}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff'
  },
  swipeAction: {
    backgroundColor: '#27ae60',
    justifyContent: 'center',
    alignItems: 'center',
    width: 80
  },
  swipeActionText: {
    color: '#fff',
    fontWeight: 'bold'
  }
});
```

## 6. Dark Mode

```jsx
// src/theme/ThemeProvider.jsx
import { createContext, useState, useContext } from 'react';
import { useColorScheme } from 'react-native';

const ThemeContext = createContext();

export const lightTheme = {
  background: '#ffffff',
  text: '#000000',
  primary: '#e74c3c',
  secondary: '#95a5a6',
  card: '#f8f9fa'
};

export const darkTheme = {
  background: '#1a1a1a',
  text: '#ffffff',
  primary: '#e74c3c',
  secondary: '#7f8c8d',
  card: '#2c2c2c'
};

export function ThemeProvider({ children }) {
  const systemTheme = useColorScheme();
  const [isDark, setIsDark] = useState(systemTheme === 'dark');
  
  const theme = isDark ? darkTheme : lightTheme;
  
  return (
    <ThemeContext.Provider value={{ theme, isDark, toggleTheme: () => setIsDark(!isDark) }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

## 7. Оптимизация производительности

### Мемоизация компонентов

```jsx
import { memo } from 'react';

const MenuCard = memo(({ item, onPress }) => {
  return (
    <TouchableOpacity onPress={onPress}>
      <Image source={{ uri: item.imageUrl }} />
      <Text>{item.name}</Text>
      <Text>{item.price} ₽</Text>
    </TouchableOpacity>
  );
}, (prevProps, nextProps) => {
  return prevProps.item.id === nextProps.item.id;
});
```

### FlatList оптимизация

```jsx
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={item => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index
  })}
/>
```

## 8. Тестирование

```jsx
// __tests__/HomeScreen.test.jsx
import { render, fireEvent } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import HomeScreen from '../src/screens/HomeScreen';

const mockStore = configureStore([]);

describe('HomeScreen', () => {
  it('renders promo items', () => {
    const store = mockStore({
      menu: {
        promoItems: [
          { id: '1', name: 'Шаурма за 5р', promoPrice: 5 }
        ],
        loading: false
      }
    });
    
    const { getByText } = render(
      <Provider store={store}>
        <HomeScreen />
      </Provider>
    );
    
    expect(getByText('Шаурма за 5р')).toBeTruthy();
  });
});
```

## Ссылки

- [Backend реализация](03_backend_implementation.md)
- [Web Frontend](04_web_frontend.md)
- [Тестирование](06_testing_ci_cd.md)

