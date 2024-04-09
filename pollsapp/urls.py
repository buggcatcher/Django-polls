# importo la funzione path per il percorso
from django.urls import path

# importo views dalla cartella corrente
from . import views

# creo la variabile urlpatterns che contiene la lista dei percorsi
# la root ('') si riferirà a view.index che andrà a prendere il
# messaggio alla linea 34 di views.py
app_name = 'pollsapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
