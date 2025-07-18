import 'package:flutter/material.dart';
import 'plant_details_screen.dart';
import 'image_upload_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PlantSync 🌿'),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to PlantSync!',
              style: Theme.of(context).textTheme.titleLarge,

            ),
            SizedBox(height: 20),
            Image.asset(
              'assets/plant_logo.png', // Ensure this image exists in assets
              height: 150,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => PlantDetailsScreen()),
                );
              },
              child: Text('🌱 View Plants'),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ImageUploadScreen()),
                );
              },
              child: Text('📸 Upload Plant Image'),
            ),
          ],
        ),
      ),
    );
  }
}
