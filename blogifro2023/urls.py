from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('postagens.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Blog IFRO 2023"
admin.site.site_title = "Meu Blog"
admin.site.index_title = "Administração do Blog"
