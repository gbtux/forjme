from django import forms
from django.forms import ModelForm
from dashboard.models import News

class ProjectForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField ( widget=forms.widgets.Textarea() )


class ChatForm(forms.Form):
	title = forms.CharField()	

class NewsForm(forms.Form):
	title = forms.CharField()
	content = forms.CharField ( widget=forms.widgets.Textarea() )

#class NewsEditForm(ModelForm):
#	class Meta:
#		model = News
