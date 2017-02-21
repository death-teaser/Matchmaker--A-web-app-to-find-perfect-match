from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from questions.models import Question
from .forms import ContactForm, SignUpForm
from .models import SignUp


def home(request):
    title = 'Welcome'
    form = SignUpForm(request.POST or None)
    context = {
        "title":  title,
        "form":form,
    }
    if form.is_valid():
        #form.save()
        instance = form.save(commit=False)
        if not instance.full_name:
            instance.full_name = "Unknown"
        instance.save()
        context = {
            "title": "Thank You"
        }
    return render(request,"home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    title = 'Contact us'
    context = {"form":form,
               "title":title,
    }
    if form.is_valid():
        email = form.cleaned_data.get("email")
        from_message = form.cleaned_data.get("message")
        from_full_name = form.cleaned_data.get("full_name")
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s: %s via %s"%(
            from_full_name,
            from_message,
            email)

        send_mail(subject,
            contact_message,
             from_email,
             to_email,
             fail_silently=True)

    return render(request,"forms.html",context)

def about(request):
    return render(request, "about.html")
