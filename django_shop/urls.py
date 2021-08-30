from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    #path('auth/', include('djoser.urls.jwt')),

    path('api/v1/', include('food.urls')),
    path('api/v1/', include('order.urls')),
    path('api/v1/', include('report.urls')),
]
