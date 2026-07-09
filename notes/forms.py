from django import forms 
from notes.models import AboutUs,ContactUs


class Aboutus(forms.Form):
    name = forms.CharField(label="Your Name",max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea)
    
class AboutusForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = '__all__'
        
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"        
    