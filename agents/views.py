from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail
import random


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agentList.html"

    def get_queryset(self):
        organisations = self.request.user.userprofile
        return Agent.objects.filter(organisations=organisations)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agentCreation.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 10000)}")
        user.save()
        Agent.objects.create(
            user=user, organisations=self.request.user.userprofile
        )
        send_mail(
            subject="you are invited to be as an agent",
            message="Please come login and start working",
            from_email="admin@gmail.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agentDetail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisations = self.request.user.userprofile
        return Agent.objects.filter(organisations=organisations)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agentUpdate.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisations = self.request.user.userprofile
        return Agent.objects.filter(organisations=organisations)


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agentDelete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisations = self.request.user.userprofile
        return Agent.objects.filter(organisations=organisations)


