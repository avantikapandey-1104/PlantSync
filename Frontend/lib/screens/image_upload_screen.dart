import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';

class ImageUploadScreen extends StatefulWidget {
  @override
  _ImageUploadScreenState createState() => _ImageUploadScreenState();
}

class _ImageUploadScreenState extends State<ImageUploadScreen> {
  File? _image;
  final picker = ImagePicker();
  String? _prediction;
  String? _confidence;

  // Pick image from gallery or camera
  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _prediction = null;
        _confidence = null;
      });
    }
  }

  // Upload image to Django API
  Future<void> _uploadImage() async {
    if (_image == null) return;

    final uri = Uri.parse("https://1094-103-120-30-54.ngrok-free.app/upload-image/"); // ✅ Replace with your correct URL

    final request = http.MultipartRequest('POST', uri);
    request.files.add(await http.MultipartFile.fromPath(
      'image',
      _image!.path,
      filename: basename(_image!.path),
    ));

    try {
      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final result = jsonDecode(responseBody);
        setState(() {
          _prediction = result['prediction'] ?? "No prediction";
          _confidence = result['confidence'] ?? "N/A";
        });
      } else {
        setState(() {
          _prediction = "Upload failed: ${response.statusCode}";
          _confidence = null;
        });
      }
    } catch (e) {
      setState(() {
        _prediction = "Error: $e";
        _confidence = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Plant Disease Detection")),//
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            _image != null
                ? Image.file(_image!, height: 200)
                : Text("No image selected", style: TextStyle(fontSize: 16)),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  child: Text("Pick from Gallery"),
                ),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: () => _pickImage(ImageSource.camera),
                  child: Text("Capture Image"),
                ),
              ],
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _uploadImage,
              child: Text("Upload and Predict"),
            ),
            const SizedBox(height: 20),
            if (_prediction != null) ...[
              Text("Prediction: $_prediction", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              if (_confidence != null)
                Text("Confidence: $_confidence", style: TextStyle(fontSize: 16, color: Colors.grey[700])),
            ]
          ],
        ),
      ),
    );
  }
}
