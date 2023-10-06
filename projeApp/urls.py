from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# uygulamadan viewsleri çağır
from siteapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', giris, name="loginpage"),
    path('logout', cikis, name="logoutpage"),
    path('register', kayitOl, name='registerpage'),
    path('', homepage, name='homepage'),
    path('profile/<str:profileName>', profile, name='profilepage'),
    path('share-tweet/', share_tweet, name='tweet'),
    path('profile_edit', edit_bio, name='edit-profile'),
    path('edit-tweet/<uuid:post_id>', edit_tweet, name='edit_tweet'),
    path('post/delete/<uuid:post_id>', delete_post, name='delete_post'),
    path('create_comment/<uuid:post_id>', create_comment, name='create_comment'),
    path('like-post', like, name='like-post'),
    path('edit-comment/<uuid:comment_id>', edit_comment, name='edit-comment'),
    path('delete-comment/<uuid:comment_id>', delete_comment, name='delete-comment'),
    path('report_comment/<uuid:comment_id>/', report_comment, name='report_comment'),
    path('report_tweet/<uuid:tweet_id>/', report_tweet, name='report_tweet'),
    path('ban_user/<str:username>/', ban_user, name='ban_user'),
    path('approve_user/<str:user_id>/', approve_user, name='approve_user'),
    path('grant_moderator/<str:user_id>/',grant_moderator, name='grant_moderator'),
    path('revoke_moderator/<str:user_id>/', revoke_moderator, name='revoke_moderator'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)