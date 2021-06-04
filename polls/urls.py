from django.urls import path
from . import views as v
from django.contrib.auth import views


app_name = 'polls'
urlpatterns = [
    path('', v.IndexView.as_view(), name='index'),
    path('<int:pk>/', v.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', v.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', v.vote, name='vote'),
    path('<int:question_id>/delete/', v.delete, name='delete'),
    path('login/', v.LoginView.as_view(), name='login'),
    path('logout/', v.LogoutView.as_view(), name='logout'),
    path('registration/', v.RegistrationView.as_view(), name='registration'),
    path('account/', v.account, name='account'),
    path('account/<int:user_id>/', v.user_account, name='user_account'),
    path('account/<int:user_id>/edit/', v.edit_account, name='edit'),
    path('account/<int:user_id>/create/', v.create, name='create'),
]
