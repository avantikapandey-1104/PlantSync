import 'package:flutter/material.dart';

class PlantDetailsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Plant Details'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Plant Name: Aloe Vera',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Image.asset(
             'assets/images/alovera.png',
              height: 200,
              fit: BoxFit.cover,
            ),


            SizedBox(height: 20),
            Text(
              'Watering: Once every 2 weeks\nSunlight: Indirect sunlight\nSoil: Well-draining soil',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
