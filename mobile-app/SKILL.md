# Mobile App Development Skill

> 모바일 앱 개발 전문가 - React Native, Flutter, iOS, Android

## Triggers
- "앱", "모바일", "앱 개발"
- "React Native", "리액트 네이티브"
- "Flutter", "플러터"
- "iOS", "안드로이드", "Android"
- "앱스토어", "플레이스토어"

## Capabilities

### 1. React Native

#### 프로젝트 설정
```bash
# Expo (권장 - 빠른 시작)
npx create-expo-app my-app
cd my-app
npx expo start

# React Native CLI
npx react-native init MyApp
cd MyApp
npx react-native run-ios    # iOS
npx react-native run-android # Android
```

#### 컴포넌트 예시
```tsx
// App.tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  FlatList,
  SafeAreaView,
} from 'react-native';

interface Item {
  id: string;
  title: string;
}

export default function App() {
  const [items, setItems] = useState<Item[]>([
    { id: '1', title: 'Item 1' },
    { id: '2', title: 'Item 2' },
  ]);

  const renderItem = ({ item }: { item: Item }) => (
    <TouchableOpacity style={styles.item}>
      <Text style={styles.itemText}>{item.title}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.header}>My App</Text>
      <FlatList
        data={items}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    padding: 16,
  },
  item: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  itemText: {
    fontSize: 16,
  },
});
```

#### 네비게이션
```tsx
// navigation/AppNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Main" component={HomeTabs} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### 2. Flutter

#### 프로젝트 설정
```bash
flutter create my_app
cd my_app
flutter run
```

#### 위젯 예시
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
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

#### 상태 관리 (Riverpod)
```dart
// providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
}

// main.dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ProviderScope(
      child: MaterialApp(
        home: CounterPage(),
      ),
    );
  }
}

class CounterPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Scaffold(
      body: Center(child: Text('$count')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(counterProvider.notifier).increment(),
        child: Icon(Icons.add),
      ),
    );
  }
}
```

### 3. 공통 기능 구현

#### 로컬 저장소
```tsx
// React Native - AsyncStorage
import AsyncStorage from '@react-native-async-storage/async-storage';

const storeData = async (key: string, value: string) => {
  await AsyncStorage.setItem(key, value);
};

const getData = async (key: string) => {
  return await AsyncStorage.getItem(key);
};
```

```dart
// Flutter - SharedPreferences
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

#### API 호출
```tsx
// React Native
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
});

export const fetchUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};
```

```dart
// Flutter
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<User>> fetchUsers() async {
  final response = await http.get(Uri.parse('https://api.example.com/users'));

  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => User.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load users');
  }
}
```

### 4. 앱 스토어 배포

#### iOS (App Store)
```yaml
checklist:
  - [ ] Apple Developer 계정 ($99/년)
  - [ ] App Store Connect 앱 생성
  - [ ] 인증서 및 프로비저닝 프로필
  - [ ] 스크린샷 (6.5", 5.5")
  - [ ] 앱 아이콘 (1024x1024)
  - [ ] 개인정보 처리방침 URL
  - [ ] 앱 심사 제출

commands:
  - flutter build ios --release
  - xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -sdk iphoneos archive
```

#### Android (Play Store)
```yaml
checklist:
  - [ ] Google Play Developer 계정 ($25)
  - [ ] 서명 키 생성 (keystore)
  - [ ] 스크린샷 (phone, 7" tablet, 10" tablet)
  - [ ] 고해상도 아이콘 (512x512)
  - [ ] 기능 그래픽 (1024x500)
  - [ ] 개인정보 처리방침 URL
  - [ ] 앱 심사 제출

commands:
  - flutter build appbundle --release
  - keytool -genkey -v -keystore upload-keystore.jks -alias upload -keyalg RSA
```

### 5. 프로젝트 구조

```
src/
├── components/          # 재사용 컴포넌트
│   ├── common/
│   └── screens/
├── navigation/          # 네비게이션 설정
├── screens/             # 화면 컴포넌트
├── services/            # API, 로컬 저장소
├── hooks/               # 커스텀 훅
├── stores/              # 상태 관리
├── utils/               # 유틸리티 함수
├── types/               # TypeScript 타입
└── assets/              # 이미지, 폰트
```
