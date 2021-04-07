from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listapersonajes', views.personajes2, name = 'personajes2'),
    path('<str:personaje>', views.personajes, name='personajes'),
    path('episodios/<int:episode_id>', views.detalles_episodio, name = 'detalles_episodio'),
    path('<str:serie>/<int:num_temporada>', views.episodios, name = 'episodios'),
]