from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Company
from .forms import CompanyForm

class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Company.objects.filter(is_verified=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_jobs'] = self.object.jobs.filter(status='active')[:5]
        return context

class CompanyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        return self.request.user.user_type == 'employer' and not hasattr(self.request.user, 'company')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Company profile created successfully!')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        if self.request.user.user_type != 'employer':
            messages.error(self.request, 'Only employers can create company profiles.')
        else:
            messages.error(self.request, 'You already have a company profile.')
        return redirect('home')

class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        return self.get_object().owner == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Company profile updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()