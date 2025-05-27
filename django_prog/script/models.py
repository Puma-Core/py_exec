from django.db import models
from django_prog.task.script import run_script
from aiohttp import ClientSession

class Script(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self):
        run_script.delay(script_code=self.content, )
        super().save()
