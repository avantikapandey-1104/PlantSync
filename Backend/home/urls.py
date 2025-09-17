from django.urls import path
from .views import homepage, upload_image, UserPlantListCreate, UserPlantDetail, ReminderListCreate, ReminderDetail, NotificationList, MarkNotificationRead

urlpatterns = [
    path('', homepage, name='home'),
    path('upload-image/', upload_image, name='upload_image'),

    # UserPlant endpoints
    path('userplants/', UserPlantListCreate.as_view(), name='userplant_list_create'),
    path('userplants/<int:pk>/', UserPlantDetail.as_view(), name='userplant_detail'),

    # Reminder endpoints
    path('reminders/', ReminderListCreate.as_view(), name='reminder_list_create'),
    path('reminders/<int:pk>/', ReminderDetail.as_view(), name='reminder_detail'),

    # Notifications
    path('notifications/', NotificationList.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', MarkNotificationRead.as_view(), name='notification_mark_read'),
]
