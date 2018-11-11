from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import *
from datetime import datetime
import random

QUESTIONS = [
    "Interested",
    "Distressed",
    "Excited",
    "Upset",
    "Strong",
    "Guilty",
    "Scared",
    "Hostile",
    "Ethusiastic",
    "Proud",
    "Irritable",
    "Alert",
    "Ashamed",
    "Inspired",
    "Nervous",
    "Determined",
    "Attentive",
    "Jittery",
    "Active",
    "Afraid"
]

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
        context['email'] = email
        context['age'] = age
        context['gender'] = gender
        context['location'] = location

        if not email or not age or not gender or not location:
            context['error'] = "Please answer all the questions"
            return render(request, 'enrollment.html', context)
        else:
            r = Respondent.objects.filter(email = email)
            if False:
                context['error'] = "You have already done this experiment"
                return render(request, 'enrollment.html', context)
            else:
                results = randomize(age, gender, location)
                r = Respondent.objects.create(email = email, gender =gender, age=age, location=location,
                                              enrollment_date=datetime.now(), group=results,
                                              level=1
                                              )
                r.save()
                request.session['respondent'] = r.id
                request.session['group'] = results

                if results == "ROXO" or results == "ROO":
                    return redirect('/pre/')
                elif results == "RXO" :
                    return redirect('/treat/')
                elif results == "RO":
                    return redirect('/control/')
    else:
        return render(request, 'enrollment.html', context)

def pretreatment(request):
    context = {"questions": QUESTIONS}
    if request.method == "POST":
        for key in request.POST:
            respondent_id = request.session.get("respondent")
            answer = request.POST[key][0]
            if key in QUESTIONS:
                p = Panas.objects.filter(respondent_id = respondent_id, pre_post="pre", question=key)
                if p:
                    p[0].answer = answer
                    p[0].save()
                else:
                    Panas.objects.create(respondent_id = respondent_id, pre_post="pre", question=key, answer=answer).save()
        group = request.session.get("group")
        if group == "ROXO" or group == "RXO":
            return redirect('/treat/')
        else:
            return redirect('/control/')
    else:
        return render(request, 'pre.html', context)


def treatment(request):
    context = {}
    group = request.session.get("group")
    return render(request, 'treat.html', context)

def control(request):
    context = {}
    group = request.session.get("group")
    return render(request, 'control.html', context)

def final(request):
    return render(request, 'final.html')

def posttreatment(request):
    context = {"questions": QUESTIONS}
    if request.method == "POST":
        for key in request.POST:
            respondent_id = request.session.get("respondent")
            answer = request.POST[key][0]
            if key in QUESTIONS:
                p = Panas.objects.filter(respondent_id = respondent_id, pre_post="post", question=key)
                if p:
                    p[0].answer = answer
                    p[0].save()
                else:
                    Panas.objects.create(respondent_id = respondent_id, pre_post="post", question=key, answer=answer).save()
        return redirect('/final/')
    else:
        return render(request, 'post.html', context)

def randomize(age, gender, location):
    groups = ["ROXO", "RXO", "ROO", "RO"]
    i = random.randint(0,3)
    print(i)
    return groups[i]