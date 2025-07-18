import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(PlantSyncApp());
}

class PlantSyncApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'PlantSync',
      theme: ThemeData(
        primarySwatch: Colors.green, // Green Theme
        scaffoldBackgroundColor: Colors.green.shade50, // Light green background
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.green.shade700, // Dark green app bar
          foregroundColor: Colors.white,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green.shade600, // Button color
            foregroundColor: Colors.white, // Button text color
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12), // Rounded corners
            ),
          ),
        ),
        textTheme: TextTheme(
          titleLarge: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.green.shade900),
          bodyLarge: TextStyle(fontSize: 16, color: Colors.green.shade800),

        ),
      ),
      home: HomeScreen(),
    );
  }
}
