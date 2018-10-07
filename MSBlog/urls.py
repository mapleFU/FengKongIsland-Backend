from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .users.views import UserViewSet, UserCreateViewSet, get_upload_token
from .blog.views import PostViewSet, TagCreateViewSet, TagReadViewSet, DirectoryViewSet, \
    get_root_directories, RelatedTagPostViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'posts', PostViewSet)

router.register(r'tags', TagReadViewSet)
router.register(r'tags', TagCreateViewSet)

router.register(r'directory', DirectoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    # path(r'^api-token-auth/', obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/upload-image-token/', get_upload_token),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    path(r'api/v1/root_directories/', get_root_directories),
    re_path(r'api/v1/tags/(?P<tag_uuid>.+)/posts/$', RelatedTagPostViewSet.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
