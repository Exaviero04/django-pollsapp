from django.shortcuts import render

# Create your views here.
from .models import  Question,Choice
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import  generic
# from django.http import Http404


# def index(request):
#     latest_question_list = Question.objects.order_by('pub_date')[:]
#     template = loader.get_template('actual_polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
#
# def index_render(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'actual_polls/index.html', context)
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'actual_polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'actual_polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'actual_polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'actual_polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'actual_polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))