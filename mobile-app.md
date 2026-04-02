---
description: 모바일 앱 개발. "앱", "모바일", "React Native", "Flutter", "iOS", "안드로이드" 트리거.
---

# 모바일 앱 개발

## React Native

### 프로젝트 생성
```bash
# Expo (권장)
npx create-expo-app@latest my-app
cd my-app
npx expo start

# React Native CLI
npx react-native init MyApp
cd MyApp
npx react-native run-android  # 또는 run-ios
```

### 기본 구조 (Expo)
```
my-app/
├── app/                    # App Router (Expo Router)
│   ├── (tabs)/
│   │   ├── index.tsx      # 홈 탭
│   │   ├── explore.tsx    # 탐색 탭
│   │   └── _layout.tsx    # 탭 레이아웃
│   ├── _layout.tsx        # 루트 레이아웃
│   └── +not-found.tsx
├── components/
├── constants/
├── hooks/
└── assets/
```

### 기본 컴포넌트
```tsx
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image } from 'react-native';
import { useState } from 'react';

export default function HomeScreen() {
  const [count, setCount] = useState(0);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Image
          source={{ uri: 'https://example.com/image.png' }}
          style={styles.image}
        />
        <Text style={styles.title}>Welcome!</Text>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={() => setCount(c => c + 1)}
      >
        <Text style={styles.buttonText}>Count: {count}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    alignItems: 'center',
    padding: 20,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 50,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 10,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    margin: 20,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
```

### 네비게이션 (Expo Router)
```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  );
}

// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <Ionicons name="home" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <Ionicons name="person" size={24} color={color} />,
        }}
      />
    </Tabs>
  );
}
```

### API 호출
```tsx
import { useEffect, useState } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

export function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('https://api.example.com/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { users, loading, error };
}
```

## Flutter

### 프로젝트 생성
```bash
flutter create my_app
cd my_app
flutter run
```

### 기본 구조
```
my_app/
├── lib/
│   ├── main.dart
│   ├── screens/
│   ├── widgets/
│   ├── models/
│   ├── services/
│   └── providers/
├── pubspec.yaml
└── assets/
```

### 기본 앱
```dart
// lib/main.dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('You have pushed the button:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### 상태관리 (Provider)
```dart
// lib/providers/counter_provider.dart
import 'package:flutter/foundation.dart';

class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }
}

// main.dart
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => CounterProvider(),
      child: const MyApp(),
    ),
  );
}

// 사용
Consumer<CounterProvider>(
  builder: (context, counter, child) {
    return Text('${counter.count}');
  },
)
```

### HTTP 요청 (Dio)
```dart
// pubspec.yaml
dependencies:
  dio: ^5.0.0

// lib/services/api_service.dart
import 'package:dio/dio.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 3),
  ));

  Future<List<User>> getUsers() async {
    try {
      final response = await _dio.get('/users');
      return (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Failed to load users');
    }
  }
}
```

## 공통 기능

### 로컬 저장소
```tsx
// React Native (AsyncStorage)
import AsyncStorage from '@react-native-async-storage/async-storage';

const storeData = async (key: string, value: any) => {
  await AsyncStorage.setItem(key, JSON.stringify(value));
};

const getData = async (key: string) => {
  const value = await AsyncStorage.getItem(key);
  return value ? JSON.parse(value) : null;
};
```

```dart
// Flutter (SharedPreferences)
import 'package:shared_preferences/shared_preferences.dart';

Future<void> saveData(String key, String value) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString(key, value);
}

Future<String?> getData(String key) async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString(key);
}
```

### 푸시 알림
```bash
# React Native
npx expo install expo-notifications

# Flutter
flutter pub add firebase_messaging
```

### 앱 빌드
```bash
# React Native (Expo)
eas build --platform android
eas build --platform ios

# Flutter
flutter build apk --release
flutter build ios --release
```

$ARGUMENTS
