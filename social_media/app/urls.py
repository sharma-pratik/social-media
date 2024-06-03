from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('friend-request/', FriendRequestCreateUpdateView.as_view(), name='friend-request-create-update'),
    path('friend-request/<int:pk>/', FriendRequestCreateUpdateView.as_view(), name='friend-request-update'),
    path('list-friends/', ListFriendRequestListView.as_view(), name='list-friend'),
    path('user-search/', UserSearchView.as_view(), name='user-search'),

]
