from django.conf.urls.defaults import *

urlpatterns = patterns('django_foaf.views',
     (r'^$', 'index'),
     #~ view profile from url
     (r'^view/', 'render_foaf'),
     #~ edit profile
     (r'^edit_profile/post/', 'edit_foaf_post'),
     (r'^edit_profile/step_2/', 'edit_foaf_step2'),
     (r'^edit_profile/', 'edit_foaf'),
     (r'^import/', 'import_foaf'),
)
