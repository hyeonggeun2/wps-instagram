from django.contrib import admin
from django.urls import path, include

from config.views import index

urlpatterns = [
  path('admin/', admin.site.urls),
  path('members/', include('members.urls')),
  path('posts/', include('posts.urls')),
  path('', index, name='index')
]