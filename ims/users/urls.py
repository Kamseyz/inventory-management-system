from django.urls import path
from .views import IndexPage, LoginUser, logout_user,login_form_partial

urlpatterns = [
    path('',IndexPage.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    # load login partial
    path('login-form/', login_form_partial, name = 'login_form_partial'),
    path('logout/', logout_user, name='logout'),
]
