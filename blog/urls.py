from django.urls import path
from . import views #Veut dire "accède à views depuis ce même dossier"

urlpatterns = [
    #On arrive ici via my_site.urls.py (my_site étant le répertoire central en quelques sorte)
    path('',views.StartingPageView.as_view(), name = 'starting-page'),
    path('posts',views.PostsView.as_view(), name = 'posts-page'),
    path('posts/<slug:slug>',views.PostDetailView.as_view(), name = 'post-detail-page'),
    path('read-later',views.ReadLaterView.as_view(), name = 'read-later')
    ]