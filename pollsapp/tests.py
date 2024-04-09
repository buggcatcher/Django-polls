import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# nella shell di python identifico un bug, le cose future non sono recenti
# >>> future_question.was_published_recently()
# mi da come output True invece che False, per questo e altri bug è giusto
# creare dei test automatizzati per far rispettare il mio codice da altri
# developers e per risparmiare tempo in futuro!
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

#  restituisce False per le domande più vecchie di un giorno
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

#  restituisce True per le domande pubblicate nell'ultimo giorno
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# crea una domanda con il question_text e il numero di giorni di distanza da adesso
# negativo per le domande pubblicate in passato
# positivo per le domande che devono ancora essere pubblicate
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
#  se non ci sono domande, viene visualizzato un testo
    def test_no_questions(self):
        response = self.client.get(reverse("pollsapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessun sondaggio disponibile")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

# le domande vecchie vengono visualizzate sull'index
    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("pollsapp:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

#  le domande future non vengono visualizzate sull'index
    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("pollsapp:index"))
        self.assertContains(response, "Nessun sondaggio disponibile")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

# se esistono domande passate e future, vengono visualizzate solo le domande passate
    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("pollsapp:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

# l'index page delle domande può visualizzare più domande
    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("pollsapp:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
# la view detail di una domanda con una data di pubblicazione nel passato visualizza la domanda
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("pollsapp:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("pollsapp:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
