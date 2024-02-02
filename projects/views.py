from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


@login_required
def projects(request):
    search = request.GET.get('search')
    
    department = Department.objects.all()

    if search:
        p = Project.objects.filter(name__icontains=search)
    else:
        p = Project.objects.all()

    paginator = Paginator(p, 8)
    page = request.GET.get('page')
    project = paginator.get_page(page)

    print(p)

    context = { 'searchTerm': search,
                'projects': project,
                'departments': department
            }
    
    return render(request, 'projects.html', context=context)

@login_required
def project_details(request, id):

    # Filter the Project queryset based on the id parameter
    project = get_object_or_404(Project, id=id)

    
    return render(request, 'project_details.html', {'project':project})

@login_required
def update_project(request, id):

    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        project.name=request.POST['name']
        project.student=request.POST['student']        
        project.abstract = request.POST['abstract']
        project.save()
        return redirect('project_details', id=id)
    else:
        return render(request, 'update_project.html', {'project':project})
    


@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    return render(request, 'delete_project.html', {'project':project})




@login_required
def sorted(request, department_id):
    search = request.GET.get('search')
    department = Department.objects.all()
    if search:
        p = Project.objects.filter(name__icontains=search)
    else:
        p = Project.objects.all()
    paginator = Paginator(p, 8)
    page = request.GET.get('page')
    project = paginator.get_page(page)
    departmentId = get_object_or_404(Department, pk=department_id)
    project = Project.objects.filter(department=departmentId)
    return render(request, 'projects.html', {'searchTerm': search, 'projects': project, 'departments': department})


@login_required
def add_project(request):
    if request.method == 'POST':
        supervisor = Supervisor.objects.get(id=1)
        department = Department.objects.get(name=request.POST['department'])
        project = Project(  name=request.POST['name'],
                            student=request.POST['student'],
                            department=department,
                            supervisor=supervisor,
                            document=request.POST['document'],
                            abstract = request.POST['abstract']
                            
                            )
        project.save()
        return redirect('projects')
    else:
        department = Department.objects.all()
        supervisors = Supervisor.objects.all()
        return render(request, 'add_project.html', {'departments': department, 'supervisors':supervisors})


@login_required
def add_staff(request):
    if request.method == 'GET':
        return render(request, 'add_staff.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                staff = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                 password=request.POST['password1'])
                staff.save()
                return redirect('projects')
            except IntegrityError:
                return render(request, 'add_staff.html', {'error': 'Username already taken. Choose new username.'})
        else:
            return render(request, 'add_staff.html', {'error': 'password does not match!'})


def admin(request):
    return render(request, 'admin.html')
