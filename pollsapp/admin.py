from django.contrib import admin

# voglio che l'admin possa modificare domande e risposte
# direttamente dalla GUI sul browser e quindi:
from .models import Question

admin.site.register(Question)
