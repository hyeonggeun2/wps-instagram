from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from config import settings
from members.views import signup_view
from posts.views import post_list

schema_view = get_schema_view(
  openapi.Info(
    title='WPS Instagram API',
    default_version='v1',
    contact=openapi.Contact(email='hyeonggeun21@naver.com'),
  ),
  public=True,
)

urlpatterns_apis = [
  path('members/', include('members.urls.apis')),
  path('posts/', include('posts.urls.apis')),
]

urlpatterns = [
  path('doc/', schema_view.with_ui('redoc', cache_timeout=0)),
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