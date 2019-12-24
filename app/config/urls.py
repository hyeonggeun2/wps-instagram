"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('posts/', include('posts.urls', namespace='posts')),
    path('members/', include('members.urls', namespace='members'))
]

urlpatterns += static(
    # 앞에 /media/가 오면
    prefix=settings.MEDIA_URL,
    # 여기서 가지고 오겠다. (static 파일을 가져올 때와 마찬가지임(static 은 자동으로 동작))
    document_root=settings.MEDIA_ROOT,
)