
from django.contrib import admin

# includo il percorso
from django.urls import include, path

# aggiungo pollsapp/ e lo reindirizzo a pollsapp.urls
urlpatterns = [
    path('pollsapp/', include('pollsapp.urls')),
    path('admin/', admin.site.urls),
]
