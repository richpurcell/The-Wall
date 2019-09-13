from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.show_wall),
    url(r'^message$', views.add_message),
    url(r'^comment$', views.add_comment),
    url(r'^logout$', views.log_out),
    url(r'delete/(?P<message_id>\d+)$', views.delete_post),
]