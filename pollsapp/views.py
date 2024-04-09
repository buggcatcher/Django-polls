# INDEX PAGE

# la view è una funzione o classe che riceve una richiesta HTTP
# e restituisce una risposta HTTP. Le views sono responsabili di
# elaborare la logica dell'applicazione e di determinare cosa
# mostrare all'utente finale.        Sono spesso utilizzate per:
# 1) Gestire le richieste degli utenti: ricevono le richieste
#    degli utenti provenienti dal browser o da altre fonti e 
#    determinano come rispondere a queste richieste.
# 2) Interagire con il modello dei dati: possono recuperare, 
#    aggiornare o eliminare dati dal database utilizzando i modelli
#    definiti all'interno dell'applicazione.
# 3) Creare e restituire risposte HTTP: Le views possono generare 
#    risposte HTTP, come pagine web HTML, dati JSON o file scaricabili,
#    e inviarle al client che ha fatto la richiesta.
# Le views in Django sono associate a specifiche URL tramite il
# meccanismo di routing delle URL (URLconf), che mappa gli URL alle
# views appropriate all'interno dell'applicazione. Quando un utente fa
# una richiesta a un URL gestito da Django, il framework utilizza
# l'URLconf per determinare quale view chiamare
# per elaborare la richiesta e generare la risposta corretta.

# importo la classe HttpResponse dal modulo http di django che
# mi permette di gestire le richieste
from django.http import HttpResponse, Http404, HttpResponseRedirect

# per lavorare con il template index.html
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# definisco la variabile latest_question_list e le passo le voci
# delle domande, le ordino le ultime [5] al contrario (-)
class IndexView(generic.ListView):
    template_name = 'pollsapp/index.html'
    context_object_name = 'latest_question_list'
# aggiungo .filter(pub_date__lte=timezone.now() per escludere le domande
# settate per essere pubblicate in futuro
    def get_queryset(self):
         return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by("-pub_date")[:5]

# sto definendo il contesto per il tuo template index.html all'interno
# della vista index di django creando un dizionario con la chiave:
#'latest_question_list' il cui valore associato è latest_question_list

#   anzichè usare il template uso il render
#   template = loader.get_template('pollsapp/index.html')
#   output = ', '.join([q.question_text for q in latest_question_list])
#   e modifico httpresponse(output) così uso il template di HTML
#   return HttpResponse(template.render(context, request))
#   chatgpt dice che si potrebbe scrivere anche così:
#   return render(request, 'pollsapp/index.html', context)

# così in base alla domanda visualizzata do una view diversa
# % question_id è un dynamic datapoint
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("questa domanda non esiste")
#     return render(request, 'pollsapp/detail.html', {'question': question})
#---------------------------------------------------------------------------
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pollsapp/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollsapp/detail.html'
# esclude le domande non ancora pubblicate
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollsapp/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_chioce = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # riporta alla pagina di dettaglio con un messaggio di errore
        return render(request, 'pollsapp/detail.html', {
            'question':question,
            'error_message': "Seleziona una risposta prima di votare",
        })
    else:
        selected_chioce.votes += 1
        selected_chioce.save()
        return HttpResponseRedirect(reverse('pollsapp:results', args=(question.id,)))
