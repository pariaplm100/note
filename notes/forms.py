from django import forms 
from notes.models import AboutUs,ContactUs
from .models import Note

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

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["name", "topic"]        
