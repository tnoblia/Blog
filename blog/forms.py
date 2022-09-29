from django import forms
from .models import CommentModel, PostModel
#class CommentForm(forms.Form):
#    author = forms.CharField(label = 'Votre nom',max_length=50, required=True)
#    content = forms.CharField(label = 'commentaire',max_length= 300, required=True)
#    id = forms.IntegerField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        #You have to explicitly enter the name of the fields of Revie that need to be taken in
        #account with :
        #  fields = ['user_name', etc...]
        #But here we take all the fields so we put :
        exclude = ['post'] 
        #if we wanted all fields but not the user name.
        labels = {'author' : "Your name",
                  'content': "Your comment",
                  "author_mail" : "Your email"}
