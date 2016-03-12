from django.contrib.auth.models import User
from django import forms
from models import Chismero, Mensaje
from django.utils.html import strip_tags #buscar definicion

         
class UserCreationForm(forms.Form):
	email=forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
	password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password1'}))
	password2=forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password2'}))
	
	class Meta:
		fields = ['email', 'username', 'password1', 'password2']
        model = Chismero

	def clean_username(self): # check if username dos not exist before
		try:
			Chismero.objects.get(username=self.cleaned_data['username']) #get user from user model
		except Chismero.DoesNotExist :
			return self.cleaned_data['username']

		raise forms.ValidationError("El usuario ya existe")


	def clean(self): # check if password 1 and password2 match each other
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
			if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
				raise forms.ValidationError("passwords dont match each other")

		return self.cleaned_data
	
	
	
	def save(self): # create new user
		new_user=Chismero.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'], email=self.cleaned_data['email'])
		new_user.save()


class ChismenewForm(forms.Form):
	texto = forms.CharField(required=True, max_length=140, widget=forms.widgets.Textarea(attrs={'cols':30, 'rows':5}))
	class Meta:
		model = Mensaje
		exclude = ('username',)





	





