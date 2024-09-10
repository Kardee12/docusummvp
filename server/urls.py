from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.Authenticated import views, dashboard, chatviews
from .views.Authenticated.views import CustomLoginView
from .views.Basic import basicviews

urlpatterns = [
                  path("", basicviews.index, name="index"),
                  path("login/", basicviews.logView, name='login'),
                  path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
                  path("workspace/", views.workspace, name="workspace"),
                  path("dashboard/", dashboard.DashboardView.as_view(), name='dashboard'),
                  path('chat/create/', chatviews.createChatSession, name='create_chat'),
                  path('chat/<uuid:chat_id>/', chatviews.viewChatSession, name='chat_detail'),
                  path('chat/<uuid:chat_id>/upload/', chatviews.uploadFilesToChat, name='upload_file'),
                  path('chat/<uuid:chat_id>/rename/', chatviews.renameChat, name='rename_chat'),
                  path('chat/<uuid:chat_id>/delete/', chatviews.deleteChat, name='delete_chat'),
                  path('test_chat', chatviews.testChat, name='test_chat')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
