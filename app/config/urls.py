from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from members.views import signup_view
from posts.views import post_list

urlpatterns_apis = [
  path('members/', include('members.urls.apis')),
  path('posts/', include('posts.urls.apis')),
]

urlpatterns = [
  path('api/', include(urlpatterns_apis)),

  path('admin/', admin.site.urls),
  path('members/', include('members.urls.views')),
  path('posts/', include('posts.urls.views')),
  path('', signup_view, name='signup'),
  path('explore/tags/<tag>/', post_list, name='list-tag'),
]

urlpatterns += static(
  prefix=settings.MEDIA_URL,
  document_root=settings.MEDIA_ROOT
)