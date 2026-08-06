from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Application

class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/my_applications.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('job', 'job__company')

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'applications/application_detail.html'
    pk_url_kwarg = 'pk'
    
    def test_func(self):
        app = self.get_object()
        return self.request.user == app.applicant or self.request.user == app.job.posted_by

class ManageApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/manage_applications.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        return Application.objects.filter(job__posted_by=self.request.user).select_related('applicant', 'job')

class UpdateApplicationStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
        new_status = request.POST.get('status')
        
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        
        return redirect('applications:manage')