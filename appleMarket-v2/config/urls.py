from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 기존 사과마켓 메인
    path("", include("apps.posts.urls")),
    # 영양성분 기능
    path("nutrient/", include("nutrient.urls")),
    # 사용자 기능
    path('users/', include('apps.users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)