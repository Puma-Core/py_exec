from django import forms
from django.forms import inlineformset_factory
from django_ace import AceWidget
from django_prog.script.models import Script, Workflow, WorkflowScript


class ScriptForm(forms.ModelForm):
    content = forms.CharField(
        label="Script Content",
        widget=AceWidget(
            toolbar=False,
            mode='python',
            theme='clouds',
            width="100%",
            height="400px",
            showprintmargin=False,
            showinvisibles=True,
            usesofttabs=True,
            tabsize=4,
        ),
    )

    class Meta:
        model = Script
        fields = "__all__"


class WorkflowScriptForm(forms.ModelForm):
    script = forms.ModelChoiceField(
        queryset=Script.objects.all(),
        label="Script",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = WorkflowScript
        fields = ['script', 'order', 'is_active']
        widgets = {
            'script': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar información adicional del script en el select
        self.fields['script'].queryset = Script.objects.all()
        self.fields['script'].empty_label = "Select a script..."


class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


WorkflowScriptFormSet = inlineformset_factory(
    Workflow,
    WorkflowScript,
    form=WorkflowScriptForm,
    extra=1,  # Formularios extra vacíos
    can_delete=True,
    can_order=False,
)
