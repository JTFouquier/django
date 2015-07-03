from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question
###jennifer

from .tests import create_question

### add here if not completed?
class IndexView(generic.ListView):
    template_name = 'relationships/index.html'
    context_object_name = 'latest_question_list'   ####JENNIFER Latest question list (TODO) remove answered questions

    jennifer_drug_list = ['tylenol','clopidogrel','citalopram', 'atenolol', 'codeine', 'random_drug']
    jennifer_question_list = [""]

    for q in jennifer_question_list:
        create_question(q,0)   ###TODO remove publication date... this will become
    #TODO remove reference to "create_question" method comment

    """ 858 230
    def create_question(question_text, days):

        Creates a question with the given `question_text` published the given
        number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).

        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text,
                                       pub_date=time)
    """

    def get_queryset(self):

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'relationships/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'relationships/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'relationships/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('relationships:results', args=(p.id,)))
