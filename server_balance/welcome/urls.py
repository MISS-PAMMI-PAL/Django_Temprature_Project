from django.urls import path 
from . import views

urlpatterns = [
    path('', views.welcome_dashboard, name='welcome_dashboard_conn'),
    path('registration/', views.registration, name='registration_conn'),
    path('registrartion/', views.reg_otp_decision, name='reg_otp_decision_conn'), # add 'r'
    path('login/', views.login, name='login_conn'),
    path('logout_user/', views.logout_user, name='logout_user_conn'),
    path('forgot-pwd/', views.forgot_pwd, name='forgot_pwd_conn'),
    path('forgot_pwd/', views.forgot_pwd_otp_decision, name='forgot_pwd_otp_decision_conn'),
    
    path('data_view/', views.data_view, name='data_view_conn'),
    path('data_fatch_ajax/', views.data_fatch_ajax, name='data_fatch_ajax_conn'),

    path('Frequently-Contact/', views.freq_contact, name='freq_contact_conn'),

    path('contact/', views.alpha_contact, name='alpha_contact_conn'),
    path('rbalance/', views.alpha_rbalance, name='alpha_rbalance_conn'),

]