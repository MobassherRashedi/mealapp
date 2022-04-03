import debug_toolbar
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('meal.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

