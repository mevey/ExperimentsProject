from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #Privacy page
    context = {}
    return render(request, 'index.html', context)

def enrollment(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email", None)
        age = request.POST.get("age", None)
        gender = request.POST.get("gender", None)
        location = request.POST.get("location", None)
        if not email or not age or not gender or not location:
            context['email'] = email
            context['age'] = age
            context['gender'] = gender
            context['location'] = location
            context['err'] = "Please answer all the questions"
            return render(request, 'enrollment.html', context)
    else:
        return render(request, 'enrollment.html', context)

def pretreatment(request):
    context = {}
    return render(request, 'pre.html', context)

def treatment(request):
    context = {}
    return render(request, 'treat.html', context)
def control(request):
    context = {}
    return render(request, 'control.html', context)

def posttreatment(request):
    context = {}
    return render(request, 'post.html', context)