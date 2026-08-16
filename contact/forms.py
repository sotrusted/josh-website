from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, label='Your name')
    email = forms.EmailField(label='Your email')
    subject = forms.CharField(max_length=300, label='Subject')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}), label='Message')


class MailingListForm(forms.Form):
    name = forms.CharField(max_length=150, required=False, label='Name (optional)')
    email = forms.EmailField(label='Email address')
