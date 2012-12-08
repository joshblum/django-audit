from django.conf.urls.defaults import *

urlpatterns = patterns('dbe.todo.views',
    (r"^item_action/(done|delete|onhold)/(\d*)/$", "item_action"),
    (r"^progress/(\d*)/$", "progress"),
    (r"^onhold_done/(onhold|done)/(on|off)/(\d*)/$", "onhold_done"),
)
