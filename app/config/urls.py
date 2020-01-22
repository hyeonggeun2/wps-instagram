from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from members.views import signup_view
from posts.views import post_list

urlpatterns = [
  path('admin/', admin.site.urls),
  path('members/', include('members.urls')),
  path('posts/', include('posts.urls')),
  path('', signup_view, name='signup'),
  path('explore/tags/<tag>/', post_list, name='list-tag'),
]

urlpatterns += static(
  prefix=settings.MEDIA_URL,
  document_root=settings.MEDIA_ROOT
)