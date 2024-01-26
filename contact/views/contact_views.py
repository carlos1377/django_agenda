from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
# Create your views here.


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')[:10]

    context = {
        'contacts': contacts,
        'site_title': 'Contatos - ',
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def search(request):
    search_value = request.GET.get('q', '').strip()
    contacts = Contact.objects.filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
        )\
        .order_by('-id')

    if search_value == '':
        redirect('contact:index')

    context = {
        'contacts': contacts,
        'site_title': 'Search - '
    }

    return render(
        request,
        'contact/index.html',
        context,
    )


def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(
        Contact, pk=contact_id, show=True,
    )

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '
    # if single_contact is None:
    #     raise Http404()

    context = {
        'contact': single_contact,
        'site_title': site_title,
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
