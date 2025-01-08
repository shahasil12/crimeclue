from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('cluelogin/', views.cluelogin, name='cluelogin'),  # Login page for principal
    path('logout/', views.logout, name='logout'),
    path('tr_login/', views.teacher_login, name='teacher_login'),
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    path('upload/', views.upload_report, name='upload_report'),
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('principal/decision/<int:report_id>/', views.principal_decision, name='principal_decision'),
    path('approve-counseling/<int:report_id>/', views.approve_counseling, name='approve_counseling'),
    path('report/<int:report_id>/review/', views.review_report, name='review_report'),
    path('confirm-delete-crime-report/<int:crime_id>/', views.confirm_delete_crime_report, name='confirm_delete_crime_report'),
    path('investigator/', views.investigator, name='investigator'),
    path('submit-report/<int:crime_id>/', views.submit_report, name='submit_report'),
    path('crime-reports/', views.crime_report_table, name='crime_report_table'),
    path('investigate/', views.investigate_table, name='investigate_table'),
    path('principal_action/<int:crime_id>/', views.principal_action, name='principal_action'),
    path('register_investigator/', views.register_investigator, name='register_investigator'),
    path('delete-crime-report/<int:crime_id>/', views.delete_crime_report, name='delete_crime_report'),
    path('students/', views.student_list, name='student_list'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('register-psychologist/', views.register_psychologist, name='register_psychologist'),
    path('psychologist-login/', views.psychologist_login, name='psychologist_login'),
    path('psychologist-dashboard/', views.psychologist_dashboard, name='psychologist_dashboard'),
    path('update-council-report/', views.council_report, name='update_council_report'),
    path('psychologist-logout/', views.psychologist_logout, name='psychologist_logout'),
    path('investigator_logout/', views.investigator_logout, name='Investigator_logout'),
    path('investigator_login/', views.investigator_login, name='investigator_login'),
    path('crime/<int:crime_id>/principal_action/', views.principal_action, name='principal_action'),
    path('submit_counseling_report/<int:crime_id>/', views.submit_counseling_report, name='submit_counseling_report'),
    path('counseling_report/', views.counseling_report_page, name='counseling_report'),
    path('reports/', views.counseling_and_crime_reports, name='counseling_and_crime_reports'),
    path('crime_detail/', views.crime_detail, name='crime_detail'),
    path('home_login/', views.home_login, name='home_login'),
    path('register/', views.register, name='register'),
    path('stdreg/', views.stdreg, name='stdreg'),  # student registration
     path('stdlogin/', views.stdlogin, name='stdlogin'),
     path('view_reports/', views.view_reports, name='view_reports'),
      path('student/<int:student_id>/reports/', views.view_student_reports, name='view_student_reports'),
      path('password_reset/', views.password_reset_request, name='password_reset_request'), 
      path('password_reset/verify/<str:email>/',views.password_reset_verify, name='password_reset_verify'),
      path('update_details/',views.update_details, name='update_details'),
      path('admins/',views.admins, name='admins'),
]
