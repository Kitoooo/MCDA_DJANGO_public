from django.urls import path, include

urlpatterns = [
    path('', include(('frontend.urls', 'frontend'), namespace="frontend")),
    path('backend/', include(('backend.urls', 'backend'), namespace='backend'))
]
