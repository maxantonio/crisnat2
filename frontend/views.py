from django.shortcuts import render
import os
from django.core.mail import send_mail
import requests
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from frontend.forms import ContactForm, NewsletterForm


def index(request):
    context = {
        'title': "Crisnat - Minería ",
        'meta_description': "Crisnat, una compañia minera mexicana en crecimiento"}
    return render(request, f'frontend/{request.LANGUAGE_CODE}/index.html', context)


def nosotros(request):
    context = {
        'bg_image': "nosotros.jpeg",
        'title': _("Nosotros"),
        'meta_description': "Sobre Crisnar minería"}
    return render(request, f'frontend/{request.LANGUAGE_CODE}/nosotros.html', context)


def materiales(request):
    context = {
        'bg_image': "nosotros.jpeg",
        'title': _("Materiales"),
        'meta_description': "Nuestros materiales"}
    return render(request, f'frontend/{request.LANGUAGE_CODE}/materiales.html', context)


def sustentabilidad(request):
    context = {
        'bg_image': "nosotros.jpeg",
        'title': _("Sustentabilidad"),
        'meta_description': "Una visión sustentable de la minería"}
    return render(request, f'frontend/{request.LANGUAGE_CODE}/sustentabilidad.html', context)


def media(request):
    context = {
        'bg_image': "nosotros.jpeg",
        'title': _("Media"),
        'meta_description': "Eventos y noticias más destacadas de la industria"}
    return render(request, f'frontend/{request.LANGUAGE_CODE}/media.html', context)


def search(request):
    return render(request, f'frontend/{request.LANGUAGE_CODE}/search.html',
                  {'term': request.GET['q'], 'title': _("Resultados de la busqueda")})


def contacto(request):
    context = {
        'bg_image': "contacto.jpeg",
        'title': _("Contacto"),
        'meta_description': "Base del meta",
        'site_key': os.getenv('RECAPTCHA_SITE_KEY')
    }
    return render(request, f'frontend/{request.LANGUAGE_CODE}/contacto.html', context)


@require_POST
def contact_form(request):
    if request.is_ajax():
        form = ContactForm(request.POST)
        secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
        data = {
            'response': request.POST.get('contact_recaptcha_response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if result_json.get('success') and result_json.get('score') > 0.5 and form.is_valid():
            html_message = loader.render_to_string(
                'emails/contact.html',
                {
                    'form': form.cleaned_data,
                }
            )

            send_mail(
                'Usuario desea contactar con el administrador del sitio Crisnat',
                '',
                'crisnat@investorcloud.net',
                ['it@irstrat.com'],
                html_message=html_message
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})


from Crypto import Random
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16


def pad(data):
    length = 16 - (len(data) % 16)
    return data + chr(length) * length


def encrypt(message, passphrase):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(passphrase.encode("utf8"), AES.MODE_CFB, IV, segment_size=128)
    return base64.b64encode(IV + aes.encrypt(pad(message).encode("utf8")))


@require_POST
def newsletter_form(request):
    if request.is_ajax():
        form = NewsletterForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('email')
            cliente = 'CRISNAT'
            data = {
                'correo': encrypt(correo, 'passwordpassword').decode("utf8"),
                # encryptando correo con contraseña del cliente
                'cliente': cliente
            }
            requests.post('https://investorlists.herokuapp.com/subscribir/', json=data)
            send_mail(
                'Usuario ' + correo + ' desea subscribirse al  sitio ' + cliente,
                'Usuario con email ' + correo + " desea subscribirse al sitio " + cliente,
                'crisnat@investorcloud.net',
                ['it@irstrat.com'],
            )
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'})
