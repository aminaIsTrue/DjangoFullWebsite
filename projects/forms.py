from django import forms
from django.forms import ModelForm, fields
from .models import Project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description', 'demo_link', 'source_link','tags','featured_image']
        widgets = {'tags':forms.CheckboxSelectMultiple()}
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input',})