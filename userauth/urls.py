from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from userauth import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/',views.signup),
    path('login/', views.loginn),
    path('logoutt/', views.logoutt),
    path('upload/',views.upload),
    path('like-post/<str:id>',views.likes,name='like-post'),
    path('#<str:id>',views.home_posts),
    path('explore',views.explore),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('search-results/', views.search_results, name='search_results'),
   # path('follow/', views.follow, name='follow'),

    #path('profile/<str:id_user>/', views.profile,name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
