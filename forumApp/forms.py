from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, CHOICES_TOPIC, CHOICES_INDUSTRY
from django_select2.forms import Select2Widget

class RegisterForm(forms.Form):

    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm password")


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        #Check if the passwords match

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    topic_tag = forms.ChoiceField(
        choices=CHOICES_TOPIC, 
        widget=Select2Widget(attrs={'class': 'form-control'})
    )
    industry_tag = forms.ChoiceField(
        choices=CHOICES_INDUSTRY, 
        widget=Select2Widget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'topic_tag', 'industry_tag']


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Leave a comment...', 'autocomplete': 'off', 'style' : 'width: 100%'}),
        }