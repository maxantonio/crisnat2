from django import forms


class NewsletterForm(forms.Form):
    email = forms.EmailField(label='Correo', widget=forms.EmailInput())


class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre', widget=forms.TextInput())

    email = forms.EmailField(label='Correo', widget=forms.EmailInput())

    subject = forms.CharField(label='Tema', widget=forms.TextInput())

    phone = forms.CharField(label='Teléfono', widget=forms.TextInput())

    message = forms.CharField(label='Mensaje', widget=forms.Textarea())
