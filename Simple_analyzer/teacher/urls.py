from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("dashboard/",views.dashboard_view,name='dashboard'),
    path('signup/',views.signup_view,name='signup'),
    path("login/",views.login_view,name='login'),
    path("student/<int:stream_id>",views.view_students,name='students'),
    path("stream/<int:stream_id>/add_student/",views.add_student,name="addstudent"),
    path("addmarks/<stream>",views.add_marks, name="addmarks"),
    path("viewmarks/",views.view_marks,name="viewmarks"),
    path("selectstream/",views.select_stream,name='select_stream'),
    path("showmarks/<int:stream_id>/<int:subject_id>/<exam_term>",views.show_marks,name="showmarks"),
    path("generatereport/",views.generate_view,name="generate_view"),
    path("finalreport/<int:stream_id>/<term>",views.compute_marks,name="compute_marks")
]
