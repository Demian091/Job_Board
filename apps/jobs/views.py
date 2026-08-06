from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, F
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Job
from .forms import JobForm
from apps.applications.forms import ApplicationForm


class JobListView(ListView):
    """Home page / Job listing page"""
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Job.objects.filter(status='active', expires_at__gt=timezone.now())
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__name__icontains=search)
            )
        
        # Filters
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
            
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience_level=experience)
            
        remote = self.request.GET.get('remote')
        if remote:
            queryset = queryset.filter(is_remote=True)
            
        return queryset.select_related('company')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_jobs'] = Job.objects.filter(
            is_featured=True, status='active'
        )[:3]
        return context


class JobDetailView(DetailView):
    """Individual job detail page"""
    model = Job
    template_name = 'jobs/job_detail.html'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        Job.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = self.object.applications.filter(
                applicant=self.request.user
            ).exists()
        context['related_jobs'] = Job.objects.filter(
            company=self.object.company
        ).exclude(id=self.object.id)[:3]
        return context


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create new job posting"""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    
    def test_func(self):
        return self.request.user.user_type == 'employer'
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        form.instance.company = self.request.user.company
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('jobs:detail', kwargs={'slug': self.object.slug})


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit existing job"""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        job = self.get_object()
        return job.posted_by == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('jobs:detail', kwargs={'slug': self.object.slug})


class MyJobsView(LoginRequiredMixin, ListView):
    """Employer's job listings"""
    model = Job
    template_name = 'jobs/my_jobs.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).order_by('-created_at')


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete job posting"""
    model = Job
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('jobs:my_jobs')
    template_name = 'jobs/job_confirm_delete.html'
    
    def test_func(self):
        job = self.get_object()
        return job.posted_by == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Job deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ApplyJobView(LoginRequiredMixin, View):
    """Handle job applications"""
    def post(self, request, slug):
        job = get_object_or_404(Job, slug=slug, status='active')
        
        if request.user.user_type != 'jobseeker':
            messages.error(request, 'Only job seekers can apply for jobs.')
            return redirect('jobs:detail', slug=slug)
        
        if job.applications.filter(applicant=request.user).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('jobs:detail', slug=slug)
        
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            # Update application count
            job.applications_count = F('applications_count') + 1
            job.save()
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('applications:my_applications')
        
        messages.error(request, 'Please correct the errors below.')
        return redirect('jobs:detail', slug=slug)