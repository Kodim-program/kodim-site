from django.shortcuts import render

# Create your views here.
def projects(request):
    return render(request, "projects.html")

def projects_summer(request):
    return render(request, "summer/index.html")

def projects_miami(request):
    return render(request, "miami/index.html")

def memory_project(request):
    return render(request, 'memory/index.html')

def project_easter(request):
    return render(request, 'easter/index.html')

def project_pillows(request):
    return render(request, 'pillows/index.html')

def project_sakura_soul(request):
    return render(request, 'sakura_soul/index.html')

def project_cosmos(request):
    return render(request, 'cosmos/index.html')