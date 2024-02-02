from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/<str:id>/', views.project_details, name='project_details'),
    path('projects/<str:id>/update/', views.update_project, name='update_project'),
    path('projects/<str:id>/delete/', views.delete_project, name='delete_project'),
    path('add-projects/', views.add_project, name='add_project'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('search/', views.projects),
    path("sorted/<int:department_id>/", views.sorted, name="sorted"),
    path('admin_panel/', views.admin, name='admin_page')
]
