from django.urls import path
from adminproject import views


urlpatterns = [

    path("login", views.admin_login),
    path("captcha", views.instance_captcha),
    path("index", views.index),
    path("public_header", views.public_header),
    path("public_left", views.public_left),
    path("acticle_publish", views.acticle_publish),
    path("acticle_publish/c_id/<int:classify_id>/page/<int:p_n>", views.acticle_publish),
    path("acticle_publish_delete/d_id/<int:d_id>", views.acticle_publish_delete),
    path("acticle_push", views.acticle_push),
    path("acticle_push/m_id/<int:modify_id>", views.acticle_push),
    path("logout", views.logout),
    path("change_pwd", views.change_password),
    path("public_index", views.public_index),
    path("upload_img", views.upload_img),
    path("add_classify", views.add_classify)

]