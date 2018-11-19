from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import *
from datetime import datetime
import random, csv
import numpy as np

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

COLORS = ["blue", "purple"]


def index(request):
    return render(request, 'index.html')

def enrollment(request):
    context = {}
    if request.method == "POST":
        age = request.POST.get("age", None)
        gender = request.POST.get("gender", None)
        location = request.POST.get("location", None)
        education = request.POST.get("education", None)
        context['age'] = age
        context['gender'] = gender
        context['location'] = location
        context['education'] = location

        if not age or not gender or not location:
            context['error'] = "Please answer all the questions"
            return render(request, 'enrollment.html', context)
        else:
            pre_color, post_color = randomize_color()
            request.session['pre_color'] = pre_color
            request.session['post_color'] = post_color

            results = randomize()
            r = Respondent.objects.create(gender =gender, age=age, location=location, education=education,
                                          enrollment_date=datetime.now(), last_update=datetime.now(), group=results,
                                          level=1, post_color=post_color, pre_color=pre_color,
                                          )
            r.save()
            request.session['respondent'] = r.id
            request.session['group'] = results


            if results == "ROXO" or results == "ROO":
                return redirect('/pre/')
            else:
                return redirect('/control/')
    else:
        return render(request, 'enrollment.html', context)

def randomize():
    groups = [["ROXO", "ROO"], ["RXO", "RO"]]
    g = np.random.binomial(n=1, p=0.3)
    i = np.random.binomial(n=1, p=0.5)
    return groups[g][i]

def randomize_color():
    l = [0,1]
    random.shuffle(l)
    return (COLORS[l[0]], COLORS[l[1]] )

def pretreatment(request):
    respondent_id = request.session.get("respondent")
    try:
        r = Respondent.objects.get(id=respondent_id)
        r.last_update = datetime.now()
        r.level = 2
        r.save()
    except:
        return redirect('/enroll/')

    SHUFFLED_QUESTIONS = QUESTIONS
    random.shuffle(SHUFFLED_QUESTIONS)
    color = request.session.get("pre_color", "blue")
    context = {"questions": SHUFFLED_QUESTIONS, "color": color}

    if request.method == "POST":
        if len(request.POST) < 20:
            data = []
            for q in SHUFFLED_QUESTIONS:
                data.append({'question': q, 'answer': request.POST.get(q, None)})
            context['data'] = data
            context['error'] = "Please answer all the questions"
            return render(request, 'pre.html', context)

        for key in request.POST:
            answer = request.POST[key][0]
            if key in QUESTIONS:
                p = Panas.objects.filter(respondent_id = respondent_id, pre_post="pre", question=key)
                if p:
                    p[0].answer = answer
                    p[0].save()
                else:
                    Panas.objects.create(respondent_id = respondent_id, pre_post="pre", question=key, answer=answer).save()
        return redirect('/control/')
    else:
        return render(request, 'pre.html', context)


def treatment(request):
    context = {}
    respondent = request.session.get("respondent")
    try:
        r = Respondent.objects.get(id = respondent)
        r.last_update = datetime.now()
        r.level = 4
        r.time_in = datetime.now()
        r.save()
    except:
        return redirect('/enroll/')
    return render(request, 'treat.html', context)

def control(request):
    context = {}
    respondent = request.session.get("respondent")
    try:
        r = Respondent.objects.get(id=respondent)
        r.last_update = datetime.now()
        r.level = 3
        r.save()
    except:
        return redirect('/enroll/')

    group = request.session.get("group")
    if group == "ROXO" or group == "RXO":
        context['next'] = "/treat/"
    else:
        context['next'] = "/post/"
    return render(request, 'control.html', context)

def number_check(request):
    context = {}
    respondent = request.session.get("respondent")
    try:
        r = Respondent.objects.get(id=respondent)
        r.last_update = datetime.now()
        r.level = 5
        r.save()
    except:
        return redirect('/enroll/')

    if request.method == "POST":
        number = request.POST.get("number", None)
        r.number = number
        r.save()
        return redirect('/post/')

    return render(request, 'number_check.html', context)

def posttreatment(request):
    try:
        respondent = request.session.get("respondent")
        r = Respondent.objects.get(id=respondent)
        r.last_update = datetime.now()
        r.level = 6
        r.time_out = datetime.now()
        r.save()
    except:
        return redirect('/enroll/')

    SHUFFLED_QUESTIONS = QUESTIONS
    random.shuffle(SHUFFLED_QUESTIONS)
    color = request.session.get("post_color", "purple")
    group = request.session.get("group")
    context = {"questions": SHUFFLED_QUESTIONS, "color": color}
    if group in ["ROXO", "RXO"]:
        context['treated'] = True

    if request.method == "POST":
            if len(request.POST) < 20:
                data = []
                for q in SHUFFLED_QUESTIONS:
                    data.append({'question': q, 'answer': request.POST.get(q, None)})
                context['data'] = data
                context['error'] = "Please answer all the questions"
                return render(request, 'post.html', context)


            for key in request.POST:
                answer = request.POST[key][0]
                if key in QUESTIONS:
                    p = Panas.objects.filter(respondent_id=respondent, pre_post="post", question=key)
                    if p:
                        p[0].answer = answer
                        p[0].save()
                    else:
                        Panas.objects.create(respondent_id=respondent, pre_post="post", question=key,
                                                 answer=answer).save()
            return redirect('/final/')
    else:
        return render(request, 'post.html', context)

def final(request):
    try:
        respondent = request.session.get("respondent")
        r = Respondent.objects.get(id=respondent)
    except:
        return redirect('/enroll/')

    r.last_update = datetime.now()
    r.level = 7
    r.save()
    del request.session['respondent']
    del request.session['group']
    del request.session['pre_color']
    del request.session['post_color']

    return render(request, 'final.html')



def dash(request):
    context = {}
    res = Respondent.objects.filter()
    mt, ft, mo, fo, ac, at, roxo, rxo, roo, ro, us, ke, ind, atd, ac_complete, at_complete = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    for r in res:
        if r.gender == "male" and r.group in ["ROXO", "RXO"]:
            mt += 1
            at += 1
            if r.number == 7: atd += 1
            if r.level == 7: at_complete += 1
        if r.gender == "female" and r.group in ["ROXO", "RXO"]:
            ft += 1
            at += 1
            if r.number == 7: atd += 1
            if r.level == 7: at_complete += 1
        if r.gender == "male" and r.group in ["ROO", "RO"]:
            mo += 1
            ac += 1
            if r.level == 7: ac_complete += 1
        if r.gender == "female" and r.group in ["ROO", "RO"]:
            fo += 1
            ac += 1
        if r.group == "ROXO": roxo += 1
        if r.group == "RXO": rxo += 1
        if r.group == "ROO": roo += 1
        if r.group == "RO": ro += 1
        if r.location == "Kenya": ke += 1
        if r.location == "United States": us += 1
        if r.location == "India": ind += 1

    context['t'] = res.count()
    context['mo'] = mo
    context['mt'] = mt
    context['fo'] = fo
    context['ft'] = ft
    context['m'] = mo + mt
    context['f'] = fo + ft
    context['ac'] = at
    context['at'] = at
    context['roxo'] = roxo
    context['rxo'] = rxo
    context['roo'] = roo
    context['ro'] = ro
    context['ke'] = ke
    context['us'] = us
    context['ind'] = ind
    context['atd'] = atd # compliance
    context['at_complete'] = at_complete
    context['ac_complete'] = ac_complete

    return render(request, 'dash.html', context)

def download(request):
    positive_affect =  [x-1 for x in [1, 3, 5, 9, 10, 12, 14, 16, 17, 19]]

    header = ["respondent_id", "age", "gender", "location", "group", "enrolled", "last_update", "level", "number_check", "time_spent_in_treatment_or_control", "pre_positive_affect", "pre_negative_affect", "post_positive_affect", "post_negative_affect"]
    individual_questions = []
    for question in QUESTIONS:
        individual_questions.extend(["pre_" + question.lower(), "post_" + question.lower()])
    header.extend(individual_questions)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="experiments_data.csv"'

    writer = csv.writer(response)
    writer.writerow(header)

    respondents = Respondent.objects.filter()
    for respondent in respondents:
        try:
            t = (respondent.time_out - respondent.time_in).total_seconds()
        except:
            t = 0

        row = [respondent.id, respondent.age, respondent.gender, respondent.location, respondent.group, respondent.enrollment_date, respondent.last_update, respondent.level, respondent.number, t]
        panas_results = Panas.objects.filter(respondent = respondent)
        pre_neg_sum, pre_pos_sum, post_neg_sum, post_pos_sum = 0, 0, 0, 0
        individual_answers = [0] * len(individual_questions)
        for p in panas_results:
            i = QUESTIONS.index(str(p.question))
            if p.pre_post == "pre":
                j = individual_questions.index("pre_" + p.question.lower())
                individual_answers[j] = int(p.answer)

                if i in positive_affect: pre_pos_sum += int(p.answer)
                else: pre_neg_sum += int(p.answer)
            else:
                j = individual_questions.index("post_" + p.question.lower())
                individual_answers[j] = int(p.answer)

                if i in positive_affect: post_pos_sum += int(p.answer)
                else: post_neg_sum += int(p.answer)
        row.extend([pre_pos_sum, pre_neg_sum, post_pos_sum, post_neg_sum])
        row.extend(individual_answers)
        writer.writerow(row)

    return response
