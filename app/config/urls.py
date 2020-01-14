from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from members.views import signup_view

urlpatterns = [
  path('admin/', admin.site.urls),
  path('members/', include('members.urls')),
  path('posts/', include('posts.urls')),
  path('', signup_view, name='signup')
]

urlpatterns += static(
  prefix=settings.MEDIA_URL,
  document_root=settings.MEDIA_ROOT
)