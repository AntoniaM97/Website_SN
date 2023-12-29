from django.urls import path
from SNweb_app import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('home/', views.home, name="home"),
    path('signup/',views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    ]