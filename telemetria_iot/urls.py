from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def api_root(request):
    return JsonResponse({
        'name': 'Telemetría Maicao API',
        'version': '1.0.0',
        'description': 'Sistema de monitoreo IoT de niveles de agua',
        'status': 'online',
        'endpoints': {
            'admin': '/admin/',
            'api_users': '/api/users/',
            'api_tanks': '/api/tanks/',
            'api_readings': '/api/readings/',
            'api_alerts': '/api/alerts/',
            'api_system_logs': '/api/system/logs/',
            'authentication': '/api/token/',
            'token_refresh': '/api/token/refresh/'
        },
        'frontend': 'https://telemetria-maicao-frontend-production.up.railway.app',
        'developers': ['Florez Pedro', 'Maldonado Juan', 'Ortiz Darien'],
        'institution': 'Universidad de La Guajira',
        'project': 'Sistema de Telemetría IoT - Maicao, La Guajira'
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/tanks/', include('tanks.urls')),
    path('api/readings/', include('readings.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/system/', include('system_logs.urls')),
]