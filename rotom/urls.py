from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('achievements/', views.achievements, name='achievements'),
    path('journies/', views.journies, name='journies'),
    path('centerbased/', views.centerbased, name='centerbased'),
    path('homebased/', views.homebased, name='homebased'),
    path('ourstory/', views.ourstory, name='ourstory'),
    path('ourplan/', views.ourplan, name='ourplan'),
    path('take-action/', views.take_action, name='take_action'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('events/', views.events_view, name='events'),
    path('donate/', views.donate, name='donate'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('champions/', views.champions, name='champion'),
    path('payment/success/', views.payment_success, name='payment_success'),
    # path('feeding-registration/', views.feeding_registration, name='feeding_registration'),
    path('subscribe/', views.subscribe, name='subscribe')
]