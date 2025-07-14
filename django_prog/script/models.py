from django.db import models
from django_prog.task.script import run_script


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Execution order")
    is_active = models.BooleanField(default=True)

    scripts = models.ManyToManyField(
        "Script",
        through='WorkflowScript',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Script(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Execution order")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        run_script.delay(script_code=self.content)
        super().save(*args, **kwargs)


class WorkflowScript(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Execution order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['workflow', 'script']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.script.name}"
