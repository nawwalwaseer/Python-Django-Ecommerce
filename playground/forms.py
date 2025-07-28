from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')
    gender = forms.ChoiceField(
        choices=[('male','Male'),('female','Female'),('other','Other')],
        label = 'Gender'
    )
    country = forms.CharField(label='Country', max_length=255)
    address = forms.CharField(label='Address', max_length=255)
    