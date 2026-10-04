from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Teacher,Student,Marks,Stream,Subject
from django.forms import ModelForm,modelformset_factory

class CreateAccountForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text='', 
    )
    
    class Meta(UserCreationForm.Meta):
        model= Teacher
        fields=(
            'first_name',
            'last_name',
            'email',
            'contact',
            
            
        )
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)

            for field in self.fields.values():
                field.help_text=''


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.fields['username'].widget.attrs.update({
            'class': 'border-2 border-green-200 focus:border-green-500 bg-gray-50',
            'placeholder': 'Enter your username'
        })
        
        
        self.fields['password'].widget.attrs.update({
            'class': 'border-2 border-green-200 focus:border-green-500 bg-gray-50',
            'placeholder': '••••••••'
        })

class StudentAddForm(ModelForm):
    class Meta:
        model=Student
        fields=(
            'Admission_number',
            'first_name',
            'last_name',
            'gender',
            'subjects',
            
        )

class SetChoicesForm(forms.Form):
    subject=forms.ModelChoiceField(queryset=Subject.objects.all(),empty_label=None)
    exam_term=forms.ChoiceField(choices=Marks.TermChoices.choices)
    stream=forms.ModelChoiceField(queryset=Stream.objects.all(),empty_label=None)


class AddMarksForm(ModelForm):
    class Meta:
        model= Marks
        fields=[
            
            
            'exam_term'
        ]
        widgets={
            
            'score':forms.NumberInput(attrs={'min':0,'max':100})
        }

MarkFormSet=modelformset_factory(Marks,form=AddMarksForm,extra=0)
     
