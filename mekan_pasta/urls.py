from django.contrib import admin
from django.urls import path
from api.views import api
from web.views import torte_home, tortenkatalog, torte_erstellen, foto, update
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('torte-home', torte_home, name='torte_home'),
    path('tortenkatalog', tortenkatalog, name='tortenkatalog'),
    path('torte-erstellen', torte_erstellen, name='torte_erstellen'),
    path('foto', foto, name='foto'),
    path('update', update, name='update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
