from django import forms

from .models import Robot
from .validators import validate_data_format


class RobotCreationForm(forms.ModelForm):
    """
    Data validation form.
    """

    model = forms.CharField(validators=[validate_data_format])
    version = forms.CharField(validators=[validate_data_format])

    class Meta:
        model = Robot
        fields = ('model', 'version', 'created',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        model = self.cleaned_data.get('model')
        version = self.cleaned_data.get('version')
        
        # Creating serial based on model and version
        instance.serial = f"{model}-{version}"
        
        if commit:
            instance.save()
        
        return instance
