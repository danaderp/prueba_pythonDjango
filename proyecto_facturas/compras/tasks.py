from celery.task import Task
from celery import Celery
from django.core.mail import EmailMessage
from django.conf import settings

class SignUpTask(Task):
    def run(self, request, pdf):
        EmailMsg = EmailMessage('Prueba','Prueba de contenido',settings.EMAIL_HOST_USER,[request.POST['email']]
                               ,headers={'Reply-To':request.POST['email']})
        EmailMsg.attach('reporte_semanal.pdf', pdf, 'application/pdf')
        EmailMsg.send()