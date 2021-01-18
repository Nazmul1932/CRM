from django.shortcuts import render, redirect, reverse
from .models import Lead
from django.http import HttpResponse
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from .models import *
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landingPage(request):
    return render(request, "landing.html")



class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leadList.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organisations=user.userprofile,
                # agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisations=user.agent.organisations,
                # agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset



def leadList(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, 'leadList.html', context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leadDetail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organisations=user.userprofile,
                # agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisations=user.agent.organisations,
                # agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def leadDetail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leadDetail.html', context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leadCreate.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        send_mail(
            subject="a lead has been created",
            message="go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def leadCreate(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form': form
    }
    return render(request, 'leadCreate.html', context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leadUpdate.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


def leadUpdate(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        'lead': lead, "form": form,
    }
    return render(request, 'leadUpdate.html', context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leadDelete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)


def leadDelete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")




