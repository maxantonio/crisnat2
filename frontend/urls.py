from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('materiales', views.materiales, name='materiales'),
    path('sustentabilidad', views.sustentabilidad, name='sustentabilidad'),
    path('media', views.media, name='media'),
    path('contacto', views.contacto, name='contacto'),
    path('contact-form', views.contact_form, name='contact-form'),
    path('newsletter-form', views.newsletter_form, name='newsletter-form'),
    path('search', views.search, name='search'),
]
