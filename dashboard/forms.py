from django import forms
from django.forms import ModelForm, Textarea
from dashboard.models import News, UseCase

class ProjectForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField ( widget=forms.widgets.Textarea() )


class ChatForm(forms.Form):
	title = forms.CharField()	

class NewsForm(forms.Form):
	title = forms.CharField()
	content = forms.CharField ( widget=forms.widgets.Textarea() )

class EventForm(forms.Form):
	title = forms.CharField()
	date_start = forms.CharField(required=False)
	date_end = forms.CharField(required=False)
	color = forms.CharField()
	all_day = forms.CharField()

class UsecaseForm(ModelForm):
	
	class Meta:
		model = UseCase
		exclude = ('created_by','creation_date', 'project',)
		widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

