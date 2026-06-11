from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def redirect_to_login(request):
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('store.urls')),

    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)