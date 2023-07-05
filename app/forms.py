from django import forms
from .models import Student


class StudentCreationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['std_id','first_name','middle_name','last_name','faculty','phone','address','email']

        # widgets={
        #     'std_id':forms.TextInput(attrs={'color':'black'})
        # }