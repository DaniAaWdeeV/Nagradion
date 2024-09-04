from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.views import generic

from .models import Question, Choice

import time
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = "pools/tournament.html"
    context_object_name = "latest_qs"

    def get_queryset(self):
        '''Get 5 latest published questions'''
        now = timezone.now()
        qs = Question.objects.order_by("-pub_date")
        qs = qs.filter(pub_date__lte=now)[:5]
        return qs


def getTime(request):
    current_time = time.time()
    date_time = time.asctime()
    return HttpResponse(f'Текущее московское время (UTC+3): {time.strftime(" %j %H:%M:%S", time.localtime())}\n{date_time}')

class DetailView(generic.DetailView):
    model = Question
    template_name = "pools/details.html"

    def get_queryset(self):
        """
        Excludes questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      "pools/details.html",
                      {
                          'question': question,
                          'error_message': "You didn't select a choice",
                      },)
    else:
        selected_choice.vote = F("vote") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("pools:results", args=[question.id]))


class ResultsView(generic.DetailView):
    model = Question
    template_name = "pools/results.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
