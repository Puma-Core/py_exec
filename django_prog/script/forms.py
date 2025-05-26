from django import forms
from django_ace import AceWidget

from django_prog.script.models import Script


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
