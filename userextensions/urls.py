from django.urls import path
from userextensions import views
from userextensions.views import ajax
from userextensions.views import action

app_name = 'userextensions'

urlpatterns = [

    # list views
    path('list_recents/', views.ListRecents.as_view(), name='list_recents'),
    path('list_favorites/', views.ListFavorites.as_view(), name='list_favorites'),

    # detail views
    path('detail_user/', views.DetailUser.as_view(), name='detail_user'),

    # create views
    path('add_favorite/', views.AddFavorite.as_view(), name='add_favorite'),

    # update views
    path('set_start_page/', views.SetStartPage.as_view(), name='set_start_page'),

    # delete views
    path('delete_favorite/<int:pk>', views.DeleteFavorite.as_view(), name='delete_favorite'),
    path('delete_recent/<int:pk>', views.DeleteRecent.as_view(), name='delete_recent'),

    # custom views
    path('user_login_redirect/', views.UserLoginRedirect.as_view(), name='user_login_redirect'),
    path('manage_service_accounts/', views.ManageServiceAccounts.as_view(), name='manage_service_accounts'),

    # action views
    path('refresh_api_token', views.RefreshApiToken.as_view(), name='refresh_api_token'),
    path('refresh_srv_acct_token', views.RefreshSrvAcctApiToken.as_view(), name='refresh_srv_acct_token'),
    path('create_custom_srv_account', action.CreateCustomServiceAccount.as_view(), name='create_custom_srv_account'),
    path('create_srv_account', action.CreateServiceAccount.as_view(), name='create_srv_account'),
    path('delete_srv_account', action.DeleteServiceAccount.as_view(), name='delete_srv_account'),
    path('enable_srv_account', action.EnableServiceAccount.as_view(), name='enable_srv_account'),
    path('disable_srv_account', action.DisableServiceAccount.as_view(), name='disable_srv_account'),
    path('edit_favorite', action.EditFavorite.as_view(), name='edit_favorite'),

    # ajax views
    path('get_users_per_group', ajax.GetUsersPerGroup.as_view(), name='get_users_per_group'),
    path('get_srv_acct_token_history', ajax.GetSerivceAccountTokenHistory.as_view(), name='get_srv_acct_token_history'),
    path('show_srv_acct_token', ajax.GetSerivceAccountToken.as_view(), name='show_srv_acct_token'),

]
