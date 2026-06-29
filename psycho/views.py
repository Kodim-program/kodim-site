from django.shortcuts import render


# Create your views here.
def psycho(request):
    return render(request, "psycho.html")
