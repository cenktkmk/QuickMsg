from django import forms
from .models import *
from django.contrib.auth import get_user_model



# Kullanıcıların kayıt olabilmesi için gereklidir 

class KayitForm(forms.ModelForm):

    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'surname'}))
    username = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', "type":"password"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'e-mail'}))
     

    class Meta:

        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

        help_texts = {

            "username": None

        }


# Kullanıcıların post paylaşabilmesi için gereklidir 


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'image']



#  Kullanıcıların kendi verilerini güncelleyebilmesi için gereklidir 

class profilePage(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text="Leave this field empty if you don't want to change your password."
    )
    new_email = forms.EmailField(
        required=False,
        help_text="Leave this field empty if you don't want to change your email."
    )

    class Meta:
        model = SiteUser
        fields = ["avatar", "bio", "country", "city", "education", "birthdate"]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_new_email(self):
        new_email = self.cleaned_data.get("new_email")
        if new_email:
            if get_user_model().objects.filter(email=new_email).exists():
                raise forms.ValidationError("This email address is already in use.")
        return new_email


# Kullanıcıların kendi postlarını düzenleyebilmesi için gereklidir 

class TweetEditForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']


# Kullanıcıların yorum atabilmesi için gereklidir 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']


# KUllanıcıların yorumlarını düzenleyebilmesini sağlar

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


# Kullanıcıların yorumları raportlamasını sağlar

class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        


# Adminlerin kullanıcıyı onaylabilmesini sağlar

class ApprovalForm(forms.Form):
    approve = forms.BooleanField(label='Hesap Onayla', required=False, initial=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))