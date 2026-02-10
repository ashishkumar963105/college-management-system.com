"""
URL configuration for college_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Adwaita Mission Institute of Technology API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'contact': '/api/contact/',
            'admin_panel': '/admin/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/contact/', include('contact.urls')),
]
