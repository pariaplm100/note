from django import forms 
from notes.models import AboutUs 

class Aboutus(forms.Form):
    name = forms.CharField(label="Your Name",max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea)
    
class AboutusForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = '__all__'
    