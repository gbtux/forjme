from django import forms

class ProjectForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField ( widget=forms.widgets.Textarea() )
