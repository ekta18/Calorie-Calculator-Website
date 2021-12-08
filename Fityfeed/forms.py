from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

class fooditemForm(ModelForm):
    class Meta:
        model=Fooditem
        fields="__all__"

class addUserFooditem(ModelForm):
	fooditem_list = forms.ModelMultipleChoiceField(
    queryset=Fooditem.objects.all(),
    widget=forms.CheckboxSelectMultiple
  )
	class Meta:
		model=UserFooditem
		fields=['fooditem_list']

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class addExercise(ModelForm):
    class Meta:
        model=Exercise
        fields=['name','time','calorie']