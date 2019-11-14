from django.shortcuts import render, HttpResponseRedirect, reverse
# from django.utils import timezone

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

from django.contrib.auth.models import User
from bugTracker.models import Ticket
from bugTracker.forms import LoginForm, RegisterNewUserForm, NewTicketForm, AssignTicketForm, CompleteTicketForm  # noqa


def login_view(request):
    html = 'generic_form_view.html'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get(
                'next',
                reverse('homepage')
            ))

    form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def register_user_view(request):
    html = 'generic_form_view.html'

    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email']
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = RegisterNewUserForm()
    return render(request, html, {'form': form})


@login_required
def index(request):
    # html = 'index.html'
    html = 'index.html'

    current_user_id = request.user.id
    new = Ticket.objects.filter(status='New')
    assigned = Ticket.objects.filter(status='In Progress')
    completed = Ticket.objects.filter(status='Done')
    invalid = Ticket.objects.filter(status='Invalid')
    ticket_types = [
        ('New Tickets', new),
        ('In Progress', assigned),
        ('Completed Tickets', completed),
        ('Invalid Tickets', invalid)]

    return render(request, html, {
        'ticket_types': ticket_types,
        'current_user_id': current_user_id})


@login_required
def create_new_ticket(request):
    html = 'generic_form_view.html'

    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        ticket = form.save()
        ticket.filed_by = request.user
        ticket.save()
        return HttpResponseRedirect(reverse('homepage'))

    form = NewTicketForm()
    return render(request, html, {'form': form})


@login_required
def user_detail_view(request, id):
    html = 'user.html'

    user = User.objects.get(pk=id)
    filed = Ticket.objects.filter(filed_by=user)
    assigned = Ticket.objects.filter(assigned_to=user)
    completed = Ticket.objects.filter(completed_by=user)
    ticket_types = [
        ('Current tickets assigned to ', assigned),
        ('Tickets filed by ', filed),
        ('Tickets completed by ', completed)
    ]

    return render(request, html, {
        'user': user,
        'ticket_types': ticket_types})


@login_required
def ticket_detail_view(request, id):
    html = 'ticket.html'

    ticket = Ticket.objects.get(pk=id)
    current_user_id = request.user.id

    return render(request, html, {
        'ticket': ticket,
        'current_user_id': current_user_id})


@login_required
def ticket_edit(request, id):
    html = 'generic_form_view.html'

    instance = Ticket.objects.get(pk=id)

    if request.method == 'POST':
        form = NewTicketForm(request.POST, instance=instance)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))

    form = NewTicketForm(instance=instance)
    return render(request, html, {'form': form})


@login_required
def unassign_ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    ticket.status = 'New'
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def uncomplete_ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    ticket.status = 'In Progress'
    ticket.assigned_to = ticket.completed_by
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def assign_ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    ticket.status = 'In Progress'
    ticket.assigned_to = request.user
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # html = 'generic_form_view.html'

    # instance = Ticket.objects.get(pk=id)

    # if request.method == 'POST':
    #     form = AssignTicketForm(request.POST, instance=instance)
    #     form.save()
    #     instance.status = 'In Progress'
    #     instance.save()
    #     return HttpResponseRedirect(reverse('homepage'))

    # form = AssignTicketForm(instance=instance)
    # return render(request, html, {'form': form, 'ticket': instance})


@login_required
def complete_ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    # if request.user.id != ticket.assigned_to.id:
    #     messages.add_message(request, messages.INFO,
    #                          'You may not complete a ticket that is not assigned to you')  # noqa
    #     return HttpResponseRedirect(reverse('homepage'))
    ticket.status = 'Done'
    ticket.completed_by = ticket.assigned_to
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # html = 'generic_form_view.html'

    # instance = Ticket.objects.get(pk=id)

    # if request.method == 'POST':
    #     form = CompleteTicketForm(request.POST, instance=instance)
    #     form.save()
    #     instance.status = 'Done'
    #     instance.assigned_to = None
    #     instance.save()
    #     return HttpResponseRedirect(reverse('homepage'))

    # form = CompleteTicketForm(instance=instance)
    # return render(request, html, {'form': form, 'ticket': instance})


@login_required
def mark_ticket_invalid(request, id):
    ticket = Ticket.objects.get(pk=id)
    ticket.status = 'Invalid'
    ticket.completed_by = None
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def make_invalid_ticket_valid(request, id):
    ticket = Ticket.objects.get(pk=id)
    ticket.status = 'New'
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
