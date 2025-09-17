from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from .models import UserPlant, Reminder, Notification
from .serializers import UserPlantSerializer, ReminderSerializer, NotificationSerializer

# Load model once globally
MODEL_PATH = os.path.join('D:\\Amy folder\\AProjects\\PlantSync\\Backend\\home', 'trained_model (1).keras')
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully")
print("Model input shape:", model.input_shape)
model.summary()

# List of labels
LABELS = [
    "Apple_scab", "Apple_black_rot", "Apple_cedar_apple_rust", "Apple_healthy",
    "Blueberry_healthy", "Cherry_powdery_mildew", "Cherry_healthy",
    "Corn_gray_leaf_spot", "Corn_common_rust", "Corn_northern_leaf_blight", "Corn_healthy",
    "Grape_black_rot", "Grape_esca", "Grape_leaf_blight", "Grape_healthy",
    "Orange_huanglongbing", "Peach_bacterial_spot", "Peach_healthy",
    "Pepper_bacterial_spot", "Pepper_healthy", "Potato_early_blight",
    "Potato_late_blight", "Potato_healthy", "Raspberry_healthy", "Soybean_healthy",
    "Squash_powdery_mildew", "Strawberry_healthy", "Strawberry_leaf_scorch",
    "Tomato_bacterial_spot", "Tomato_early_blight", "Tomato_healthy", "Tomato_late_blight",
    "Tomato_leaf_mold", "Tomato_septoria_leaf_spot", "Tomato_spider_mites_two_spotted_spider_mite",
    "Tomato_target_spot", "Tomato_yellow_leaf_curl_virus", "Tomato_mosaic_virus"
]

# Disease information database
DISEASE_INFO = {
    "Apple_scab": {
        "description": "Apple scab is a fungal disease that causes dark, scabby lesions on leaves, fruit, and twigs. It spreads through spores during wet weather.",
        "care_tips": [
            "Remove and destroy infected leaves and fruit",
            "Apply fungicide sprays during bud break and petal fall",
            "Ensure good air circulation by proper pruning",
            "Avoid overhead watering to reduce humidity"
        ],
        "reminders": [
            "Apply fungicide every 7-10 days during wet periods",
            "Monitor for symptoms weekly during growing season",
            "Prune infected branches in late winter"
        ]
    },
    "Apple_black_rot": {
        "description": "Black rot is a fungal disease that affects apples, causing fruit rot and cankers on branches. It overwinters in infected wood.",
        "care_tips": [
            "Prune out infected branches and fruit mummies",
            "Apply fungicide sprays during bloom and petal fall",
            "Ensure proper tree spacing for air circulation",
            "Clean up fallen fruit and debris"
        ],
        "reminders": [
            "Prune dead wood in late winter",
            "Apply fungicide during critical growth stages",
            "Inspect trees regularly for cankers"
        ]
    },
    "Apple_cedar_apple_rust": {
        "description": "Cedar apple rust is a fungal disease that requires both apple trees and cedar trees to complete its life cycle. It causes orange spots on leaves.",
        "care_tips": [
            "Remove nearby cedar trees if possible",
            "Apply fungicide sprays during spring",
            "Plant rust-resistant apple varieties",
            "Ensure good air circulation"
        ],
        "reminders": [
            "Apply fungicide during wet spring weather",
            "Monitor for orange spore horns on cedar trees",
            "Prune infected branches immediately"
        ]
    },
    "Apple_healthy": {
        "description": "Your apple tree appears to be healthy with no visible signs of disease.",
        "care_tips": [
            "Continue regular watering and fertilization",
            "Monitor for pests and diseases regularly",
            "Prune annually for good structure",
            "Apply dormant oil spray in winter"
        ],
        "reminders": [
            "Fertilize in early spring",
            "Prune in late winter before bud break",
            "Monitor for aphids and mites"
        ]
    },
    "Blueberry_healthy": {
        "description": "Your blueberry plant appears to be healthy with no visible signs of disease.",
        "care_tips": [
            "Maintain acidic soil pH (4.5-5.5)",
            "Water consistently, keeping soil moist",
            "Mulch around plants to retain moisture",
            "Prune annually after harvest"
        ],
        "reminders": [
            "Test soil pH annually",
            "Water during dry periods",
            "Fertilize with acid-loving plant fertilizer"
        ]
    },
    "Cherry_powdery_mildew": {
        "description": "Powdery mildew appears as white, powdery spots on leaves and fruit. It thrives in humid conditions with poor air circulation.",
        "care_tips": [
            "Improve air circulation through pruning",
            "Apply fungicide sprays preventively",
            "Avoid overhead watering",
            "Remove infected plant parts"
        ],
        "reminders": [
            "Apply fungicide every 7-14 days during humid weather",
            "Prune for better air flow",
            "Monitor humidity levels"
        ]
    },
    "Cherry_healthy": {
        "description": "Your cherry tree appears to be healthy with no visible signs of disease.",
        "care_tips": [
            "Prune annually for good structure",
            "Monitor for pests like aphids",
            "Apply dormant oil spray in winter",
            "Ensure proper fertilization"
        ],
        "reminders": [
            "Prune in late winter",
            "Apply dormant oil before bud break",
            "Monitor for brown rot during fruit development"
        ]
    },
    "Corn_gray_leaf_spot": {
        "description": "Gray leaf spot is a fungal disease that causes rectangular gray lesions on corn leaves. It reduces photosynthesis and yield.",
        "care_tips": [
            "Plant resistant varieties",
            "Rotate crops to break disease cycle",
            "Apply fungicide if disease pressure is high",
            "Ensure proper plant spacing"
        ],
        "reminders": [
            "Scout fields weekly during growing season",
            "Apply fungicide at tasseling if needed",
            "Rotate crops annually"
        ]
    },
    "Corn_common_rust": {
        "description": "Common rust appears as reddish-brown pustules on both leaf surfaces. It can reduce yield significantly in severe cases.",
        "care_tips": [
            "Plant resistant varieties",
            "Apply fungicide preventively",
            "Ensure good plant nutrition",
            "Avoid excessive nitrogen fertilization"
        ],
        "reminders": [
            "Monitor for pustules weekly",
            "Apply fungicide at first sign of disease",
            "Ensure proper field drainage"
        ]
    },
    "Corn_northern_leaf_blight": {
        "description": "Northern leaf blight causes long, elliptical gray-green lesions on corn leaves. It can cause significant yield loss.",
        "care_tips": [
            "Plant resistant hybrids",
            "Apply fungicide at tasseling",
            "Practice crop rotation",
            "Ensure proper plant spacing"
        ],
        "reminders": [
            "Scout fields regularly",
            "Apply fungicide preventively",
            "Destroy crop residue after harvest"
        ]
    },
    "Corn_healthy": {
        "description": "Your corn plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Ensure proper soil fertility",
            "Monitor for pests regularly",
            "Water consistently during dry periods",
            "Practice crop rotation"
        ],
        "reminders": [
            "Fertilize based on soil tests",
            "Monitor for corn borers",
            "Ensure proper irrigation"
        ]
    },
    "Grape_black_rot": {
        "description": "Black rot is a fungal disease that causes black lesions on leaves and fruit. It can destroy entire grape clusters.",
        "care_tips": [
            "Apply fungicide sprays during growing season",
            "Remove infected fruit and leaves",
            "Ensure good air circulation",
            "Prune for sunlight penetration"
        ],
        "reminders": [
            "Apply fungicide every 7-10 days during wet weather",
            "Remove mummified fruit in winter",
            "Prune for better air flow"
        ]
    },
    "Grape_esca": {
        "description": "Esca is a fungal disease that causes internal wood decay and leaf symptoms. It can kill vines over time.",
        "care_tips": [
            "Remove infected vines immediately",
            "Avoid pruning wounds during wet weather",
            "Apply wound protectants after pruning",
            "Improve soil drainage"
        ],
        "reminders": [
            "Monitor for tiger stripe leaf symptoms",
            "Prune during dry weather",
            "Apply fungicide to pruning wounds"
        ]
    },
    "Grape_leaf_blight": {
        "description": "Leaf blight causes brown spots and lesions on grape leaves, reducing photosynthesis and fruit quality.",
        "care_tips": [
            "Apply fungicide preventively",
            "Improve air circulation through pruning",
            "Remove infected leaves",
            "Avoid overhead irrigation"
        ],
        "reminders": [
            "Apply fungicide during bud break and bloom",
            "Prune for better air flow",
            "Monitor humidity levels"
        ]
    },
    "Grape_healthy": {
        "description": "Your grape vines appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Prune annually for good structure",
            "Monitor for pests and diseases",
            "Ensure proper fertilization",
            "Provide support for vines"
        ],
        "reminders": [
            "Prune in late winter",
            "Fertilize in early spring",
            "Monitor for phylloxera"
        ]
    },
    "Orange_huanglongbing": {
        "description": "Huanglongbing (HLB) is a bacterial disease spread by psyllid insects. It causes yellowing, stunting, and fruit drop.",
        "care_tips": [
            "Remove and destroy infected trees",
            "Control psyllid populations",
            "Use disease-free planting material",
            "Monitor for symptoms regularly"
        ],
        "reminders": [
            "Inspect trees weekly for symptoms",
            "Control psyllid vectors",
            "Remove infected trees immediately"
        ]
    },
    "Peach_bacterial_spot": {
        "description": "Bacterial spot causes dark lesions on leaves, fruit, and twigs. It can cause defoliation and reduce fruit quality.",
        "care_tips": [
            "Apply copper fungicide sprays",
            "Avoid overhead watering",
            "Prune for air circulation",
            "Plant resistant varieties"
        ],
        "reminders": [
            "Apply copper sprays during wet weather",
            "Prune infected branches",
            "Monitor for leaf spots"
        ]
    },
    "Peach_healthy": {
        "description": "Your peach tree appears to be healthy with no visible signs of disease.",
        "care_tips": [
            "Prune annually for good structure",
            "Apply dormant oil spray",
            "Monitor for pests like oriental fruit moth",
            "Ensure proper fertilization"
        ],
        "reminders": [
            "Prune in late winter",
            "Apply dormant oil before bud break",
            "Thin fruit for better quality"
        ]
    },
    "Pepper_bacterial_spot": {
        "description": "Bacterial spot causes dark lesions on leaves, stems, and fruit. It can cause significant yield loss.",
        "care_tips": [
            "Apply copper fungicide sprays",
            "Avoid overhead watering",
            "Rotate crops annually",
            "Plant disease-resistant varieties"
        ],
        "reminders": [
            "Apply copper sprays preventively",
            "Monitor for water-soaked spots",
            "Rotate crops to prevent disease buildup"
        ]
    },
    "Pepper_healthy": {
        "description": "Your pepper plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Ensure consistent watering",
            "Provide support for plants",
            "Monitor for aphids and spider mites",
            "Fertilize regularly"
        ],
        "reminders": [
            "Water consistently to prevent blossom end rot",
            "Support plants as they grow",
            "Monitor for pests weekly"
        ]
    },
    "Potato_early_blight": {
        "description": "Early blight causes dark lesions with concentric rings on leaves. It can reduce yield and tuber quality.",
        "care_tips": [
            "Apply fungicide sprays preventively",
            "Avoid overhead irrigation",
            "Rotate crops annually",
            "Remove infected plant debris"
        ],
        "reminders": [
            "Apply fungicide every 7-10 days",
            "Monitor lower leaves for symptoms",
            "Destroy infected plants after harvest"
        ]
    },
    "Potato_late_blight": {
        "description": "Late blight is a devastating disease that can destroy entire potato crops. It causes dark, water-soaked lesions.",
        "care_tips": [
            "Apply fungicide preventively",
            "Avoid overhead watering",
            "Plant resistant varieties",
            "Ensure good air circulation"
        ],
        "reminders": [
            "Apply fungicide during humid weather",
            "Monitor for symptoms daily",
            "Destroy infected plants immediately"
        ]
    },
    "Potato_healthy": {
        "description": "Your potato plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Hill soil around plants as they grow",
            "Monitor for Colorado potato beetle",
            "Ensure consistent watering",
            "Fertilize appropriately"
        ],
        "reminders": [
            "Hill plants weekly",
            "Monitor for pests regularly",
            "Water during dry periods"
        ]
    },
    "Raspberry_healthy": {
        "description": "Your raspberry plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Prune annually after harvest",
            "Provide support for canes",
            "Monitor for aphids and spider mites",
            "Ensure good soil drainage"
        ],
        "reminders": [
            "Prune summer-bearing varieties in winter",
            "Fertilize in early spring",
            "Monitor for cane diseases"
        ]
    },
    "Soybean_healthy": {
        "description": "Your soybean plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Ensure proper soil fertility",
            "Monitor for pests like soybean aphids",
            "Practice crop rotation",
            "Ensure good drainage"
        ],
        "reminders": [
            "Scout for pests weekly",
            "Monitor soil moisture",
            "Test soil pH and fertility"
        ]
    },
    "Squash_powdery_mildew": {
        "description": "Powdery mildew appears as white, powdery coating on leaves. It reduces photosynthesis and fruit quality.",
        "care_tips": [
            "Apply fungicide sprays",
            "Improve air circulation",
            "Avoid overhead watering",
            "Plant resistant varieties"
        ],
        "reminders": [
            "Apply fungicide every 7-14 days during humid weather",
            "Space plants for better air flow",
            "Monitor humidity levels"
        ]
    },
    "Strawberry_healthy": {
        "description": "Your strawberry plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Renew plants every 3-4 years",
            "Apply mulch to prevent weeds",
            "Monitor for slugs and snails",
            "Ensure proper watering"
        ],
        "reminders": [
            "Renew beds with new plants",
            "Apply mulch in spring",
            "Monitor for gray mold during fruiting"
        ]
    },
    "Strawberry_leaf_scorch": {
        "description": "Leaf scorch causes reddish-brown lesions along leaf edges. It can reduce plant vigor and yield.",
        "care_tips": [
            "Apply fungicide sprays",
            "Improve air circulation",
            "Avoid overhead watering",
            "Remove infected leaves"
        ],
        "reminders": [
            "Apply fungicide preventively",
            "Prune for better air flow",
            "Monitor leaf edges for symptoms"
        ]
    },
    "Tomato_bacterial_spot": {
        "description": "Bacterial spot causes dark lesions on leaves, stems, and fruit. It can cause significant yield loss.",
        "care_tips": [
            "Apply copper fungicide sprays",
            "Avoid overhead watering",
            "Rotate crops annually",
            "Plant disease-resistant varieties"
        ],
        "reminders": [
            "Apply copper sprays during wet weather",
            "Monitor for small dark spots",
            "Rotate crops to prevent disease buildup"
        ]
    },
    "Tomato_early_blight": {
        "description": "Early blight causes dark lesions with concentric rings on leaves. It can reduce yield and fruit quality.",
        "care_tips": [
            "Apply fungicide sprays preventively",
            "Mulch around plants",
            "Avoid overhead irrigation",
            "Remove infected leaves"
        ],
        "reminders": [
            "Apply fungicide every 7-10 days",
            "Monitor lower leaves for symptoms",
            "Mulch to prevent soil splash"
        ]
    },
    "Tomato_healthy": {
        "description": "Your tomato plants appear to be healthy with no visible signs of disease.",
        "care_tips": [
            "Provide support with cages or stakes",
            "Monitor for pests like tomato hornworm",
            "Water consistently at soil level",
            "Fertilize regularly"
        ],
        "reminders": [
            "Support plants as they grow",
            "Water consistently to prevent cracking",
            "Monitor for blossom end rot"
        ]
    },
    "Tomato_late_blight": {
        "description": "Late blight is a devastating disease that can destroy tomato crops quickly. It causes dark, water-soaked lesions.",
        "care_tips": [
            "Apply fungicide preventively",
            "Avoid overhead watering",
            "Ensure good air circulation",
            "Remove infected plants immediately"
        ],
        "reminders": [
            "Apply fungicide during humid weather",
            "Monitor for symptoms daily",
            "Destroy infected plants immediately"
        ]
    },
    "Tomato_leaf_mold": {
        "description": "Leaf mold causes yellow spots on upper leaf surfaces and olive-green mold on lower surfaces. It thrives in humid conditions.",
        "care_tips": [
            "Improve air circulation through pruning",
            "Apply fungicide sprays",
            "Avoid overhead watering",
            "Space plants properly"
        ],
        "reminders": [
            "Apply fungicide every 7-14 days in humid conditions",
            "Prune for better air flow",
            "Monitor humidity levels"
        ]
    },
    "Tomato_septoria_leaf_spot": {
        "description": "Septoria leaf spot causes small, circular spots with dark borders on leaves. It can cause defoliation.",
        "care_tips": [
            "Apply fungicide sprays",
            "Mulch around plants",
            "Avoid overhead watering",
            "Remove infected leaves"
        ],
        "reminders": [
            "Apply fungicide preventively",
            "Monitor lower leaves for small spots",
            "Mulch to prevent soil splash"
        ]
    },
    "Tomato_spider_mites_two_spotted_spider_mite": {
        "description": "Two-spotted spider mites cause stippling and yellowing of leaves. They thrive in hot, dry conditions.",
        "care_tips": [
            "Increase humidity around plants",
            "Apply insecticidal soap or neem oil",
            "Avoid broad-spectrum insecticides",
            "Wash plants with strong water spray"
        ],
        "reminders": [
            "Monitor for stippling on leaves",
            "Apply insecticidal soap weekly if needed",
            "Increase humidity during hot weather"
        ]
    },
    "Tomato_target_spot": {
        "description": "Target spot causes concentric ring lesions on leaves and fruit. It can reduce yield significantly.",
        "care_tips": [
            "Apply fungicide sprays",
            "Improve air circulation",
            "Avoid overhead watering",
            "Rotate crops annually"
        ],
        "reminders": [
            "Apply fungicide preventively",
            "Monitor for concentric lesions",
            "Rotate crops to prevent disease buildup"
        ]
    },
    "Tomato_yellow_leaf_curl_virus": {
        "description": "Yellow leaf curl virus causes yellowing and curling of leaves, stunting, and reduced yield. It's spread by whiteflies.",
        "care_tips": [
            "Control whitefly populations",
            "Use reflective mulch to repel whiteflies",
            "Plant resistant varieties",
            "Remove infected plants"
        ],
        "reminders": [
            "Monitor for whiteflies weekly",
            "Apply reflective mulch early",
            "Remove infected plants immediately"
        ]
    },
    "Tomato_mosaic_virus": {
        "description": "Mosaic virus causes mottled yellow and green patterns on leaves, leaf distortion, and reduced yield.",
        "care_tips": [
            "Remove infected plants immediately",
            "Control aphids that spread the virus",
            "Disinfect tools between plants",
            "Plant virus-resistant varieties"
        ],
        "reminders": [
            "Monitor for mottled leaf patterns",
            "Control aphids regularly",
            "Disinfect tools between plants"
        ]
    }
}

# ✅ Add csrf_exempt decorator to allow external POST without CSRF token
@csrf_exempt
@api_view(['POST'])
def upload_image(request):
    try:
        print("FILES:", request.FILES)  # optional debugging
        file = request.FILES['image']
        image = Image.open(file).convert('RGB')
        image = image.resize((128, 128))

        # Convert to numpy array (NO manual /255, model already rescales)
        img_array = np.array(image).astype(np.float32)
        img_array = np.expand_dims(img_array, axis=0)  # shape: (1,100,100,3)

        print("Model input shape:", model.input_shape)
        print("Image array shape:", img_array.shape)

        # Get prediction
        prediction = model.predict(img_array)
        print("Prediction array:", prediction)

        predicted_index = np.argmax(prediction)
        confidence = round(float(np.max(prediction)) * 100, 2)

        # Debug: print all prediction probabilities with labels
        for i, prob in enumerate(prediction[0]):
            print(f"{LABELS[i]}: {prob:.4f}")

        predicted_label = LABELS[predicted_index]
        print(f"Predicted label: {predicted_label}, Confidence: {confidence}%")

        # Get disease information
        disease_info = DISEASE_INFO.get(predicted_label, {
            "description": "Disease information not available.",
            "care_tips": ["Consult a local agricultural extension service for specific recommendations."],
            "reminders": ["Monitor plant health regularly."]
        })

        return Response({
            'prediction': predicted_label,
            'confidence': f"{confidence}%",
            'description': disease_info['description'],
            'care_tips': disease_info['care_tips'],
            'reminders': disease_info['reminders']
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def homepage(request):
    return HttpResponse("""
        <div style='text-align:center; padding: 20px;'>
            <h1>🌿 Welcome to PlantSync</h1>
            <p>Upload images of your plants to detect diseases using our AI-powered model.</p>
            <img src='/static/images/plant_welcome.jpg' alt='Beautiful Plant' style='max-width: 400px; margin-top: 20px; border-radius: 10px;'/>
        </div> 
    """)

# UserPlant Views
class UserPlantListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plants = UserPlant.objects.filter(user=request.user)
        serializer = UserPlantSerializer(plants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserPlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPlantDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return UserPlant.objects.get(pk=pk, user=user)
        except UserPlant.DoesNotExist:
            return None

    def get(self, request, pk):
        plant = self.get_object(pk, request.user)
        if not plant:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserPlantSerializer(plant)
        return Response(serializer.data)

    def put(self, request, pk):
        plant = self.get_object(pk, request.user)
        if not plant:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserPlantSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plant = self.get_object(pk, request.user)
        if not plant:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Reminder Views
class ReminderListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reminders = Reminder.objects.filter(plant__user=request.user, is_active=True)
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReminderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReminderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Reminder.objects.get(pk=pk, plant__user=user)
        except Reminder.DoesNotExist:
            return None

    def get(self, request, pk):
        reminder = self.get_object(pk, request.user)
        if not reminder:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data)

    def put(self, request, pk):
        reminder = self.get_object(pk, request.user)
        if not reminder:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReminderSerializer(reminder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reminder = self.get_object(pk, request.user)
        if not reminder:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        reminder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Notification Views
@method_decorator(csrf_exempt, name='dispatch')
class NotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class MarkNotificationRead(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
