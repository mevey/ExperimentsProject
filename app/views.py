from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import *
from datetime import datetime
import random, csv

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
    random.shuffle(QUESTIONS)
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
    respondent = request.session.get("respondent")
    r = Respondent.objects.get(id = respondent)
    r.last_update = datetime.now()
    r.level = 3
    r.time_in = datetime.now()
    r.save()
    return render(request, 'treat.html', context)

def control(request):
    context = {}
    respondent = request.session.get("respondent")
    r = Respondent.objects.get(id=respondent)
    r.last_update = datetime.now()
    r.level = 4
    r.time_in = datetime.now()
    r.save()
    return render(request, 'control.html', context)

def final(request):
    try:
        respondent = request.session.get("respondent")
        r = Respondent.objects.get(id=respondent)
        r.last_update = datetime.now()
        r.level = 6
        r.time_out = datetime.now()
        r.save()
    except:
        pass
    return render(request, 'final.html')

def posttreatment(request):
    random.shuffle(QUESTIONS)
    context = {"questions": QUESTIONS}
    if request.method == "POST":
        try:
            respondent = request.session.get("respondent")
            r = Respondent.objects.get(id=respondent)
            r.last_update = datetime.now()
            r.level = 6
            r.save()
        except:
            pass

        respondent_id = request.session.get("respondent")
        for key in request.POST:
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


def download(request):
    positive_affect =  [x-1 for x in [1, 3, 5, 9, 10, 12, 14, 16, 17, 19]]

    header = ["respondent_id", "age", "gender", "location", "group", "enrolled", "last_update", "level", "time_spent_in_treatment_or_control", "pre_positive_affect", "pre_negative_affect", "post_positive_affect", "post_negative_affect"]


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="experiments_data.csv"'

    writer = csv.writer(response)
    writer.writerow(header)

    respondents = Respondent.objects.filter()
    for respondent in respondents:
        if respondent.time_out:
            t = (respondent.time_out - respondent.time_in).total_seconds()
        else:
            t = 0
        row = [respondent.id, respondent.age, respondent.gender, respondent.location, respondent.group, respondent.enrollment_date, respondent.last_update, respondent.level, t]
        panas_results = Panas.objects.filter(respondent = respondent)
        pre_neg_sum = 0
        pre_pos_sum = 0
        post_neg_sum = 0
        post_pos_sum = 0
        for p in panas_results:
            i = QUESTIONS.index(str(p.question))
            print(i)
            print(p.answer)
            if p.pre_post == "pre":
                if i in positive_affect: pre_pos_sum += int(p.answer)
                else: pre_neg_sum += int(p.answer)
            else:
                if i in positive_affect: post_pos_sum += int(p.answer)
                else: post_neg_sum += int(p.answer)
        row.extend([pre_pos_sum, pre_neg_sum, post_pos_sum, post_neg_sum])
        writer.writerow(row)

    return response
