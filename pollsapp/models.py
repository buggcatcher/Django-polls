# il modello si usa per organizzare i dati nel database. 
# è la principale fonte di informazioni sui dati, includendo 
# campi e comportamenti essenziali. Le migrazioni vengono
# create per trasferire queste definizioni nel database, 
# permettendo la creazione effettiva delle voci.
# le migrazioni sono il metodo con cui si dice a django di 
# immagazzinare le modifiche fatte ai modelli
from django.db import models
import datetime
from django.utils import timezone

# creo due classi, una per le domande e una per le risposte. è
# importante far ereditare le funzionalità alla classe Question
# dal modello Model per migrare correttamente i dati

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('pubblicato il')

# per far ritornare la stringa domanda anzichè l'oggetto domanda
    def __str__(self):
        return self.question_text
# per questo devo includere (import) timezone e datetime    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# ora che ho il modello lo esplicito in settings.py riga 46
# una volta definiti i modelli vado sul teminale e faccio
# (.. makemigrations ..) per poi (.. migrate ..)