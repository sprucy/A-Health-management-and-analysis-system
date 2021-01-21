"""healthmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from healthinfo import views
from django.views.static import serve
from django.conf.urls import url

from healthmanage.settings import MEDIA_ROOT

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('healthinfo/', include('healthinfo.urls')),
    #在setings.py中定义MEDIA_ROOT后，在url.py中必须增加medias路径，才能访问目录中的文件
    #注意如果如果setings.py中定义：MEDIA_ROOT = os.path.join(BASE_DIR,"medias")
    #                     这里为：{'document_root': MEDIA_ROOT}
    #注意如果如果setings.py中定义：MEDIA_ROOT = [os.path.join(BASE_DIR,"medias"),]
    #                     这里为：{'document_root': MEDIA_ROOT[n]},其中n为你目录列表中的实际数字
    url(r'medias/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]
