# 🌿 PlantSync: Plant Disease Detection Mobile Application

PlantSync is a full-stack AI-integrated mobile application that helps users diagnose plant diseases simply by uploading an image of a plant leaf. Powered by Flutter for the frontend, Django for the backend, and a TensorFlow deep learning model, it predicts whether the plant is healthy or affected by a disease.


📦 Project Structure
PlantSync/
├── backend/
│   ├── manage.py
│   ├── home/
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── trained_model.h5
│   └── settings.py
├── frontend/
│   └── lib/
│       └── image_upload_screen.dart
├── pubspec.yaml
└── README.md


## 📸 Demo Screenshots
![1](https://github.com/user-attachments/assets/ecb35270-401b-43ed-8ec3-0fa73533ff8b)
    ![WhatsApp Image 2025-07-18 at 23 59 15_b4707524](https://github.com/user-attachments/assets/59b297d9-28b0-4787-8b46-be71d39edb17)     ![WhatsApp Image 2025-07-18 at 23 59 14_4e3a8719](https://github.com/user-attachments/assets/8ac3c621-5df5-4cf7-a6ae-6167e5f2a6e3)


## 🚀 Live Features

✅ Upload plant image via camera or gallery  
✅ Real-time disease prediction using a trained ML model  
✅ Works on real Android devices (no emulator required)  
✅ JSON API response with prediction and confidence  
✅ Integrated image picker, HTTP networking, and TensorFlow in production-ready workflow

---

## 🔧 Tech Stack

| Layer        | Technology                             |
|--------------|----------------------------------------|
| Frontend     | Flutter (Dart)                         | 
| Backend      | Django (Python + DRF)                  |
| AI/ML Model  | TensorFlow (.h5 format)                |
| Image Upload | `http.MultipartRequest` (Flutter)      |
| Testing      | Postman                                |
    

📌 Future Enhancements
🛰 Deploy on Firebase or Heroku
🌍 Use GPS to alert regional disease outbreaks
🔔 Add watering/fertilizing reminders
📈 Analytics dashboard for predictions
🌐 Multi-language support for rural adoption
## 📱 Frontend – Flutter

**Screens:**
- 📷 Image Picker (camera + gallery)
- 🔼 Upload Button
- 🧾 Prediction Output Display


👥 Team Members
Avantika Pandey- Team Leader and Backend Developer
Aashna Jain- Machine Learning Developer
Daksh Singh- Frontend Developer



