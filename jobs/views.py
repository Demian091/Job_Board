from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application, Post, Comment, Like
from .forms import JobForm, ApplicationForm, PostForm, CommentForm
from company.models import Company ,User

def job_list(request):
    query = request.GET.get("q")  # search query
    category = request.GET.get("category")  # category filter
    
    jobs = Job.objects.all()

    # Search
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(company__name__icontains=query)
        )

    # Filter by category
    if category and category != "all":
        jobs = jobs.filter(category__iexact=category)

    categories = Job.objects.values_list("category", flat=True).distinct()
    
    return render(request, "jobs/job_list.html", {
        "jobs": jobs,
        "categories": categories,
    })
    
    
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.user.role != 'employer':
        messages.error(request, "Only employers can post jobs.")
        return redirect('job_list')

    try:
        company = request.user.company
    except Company.DoesNotExist:
        messages.error(request, "You must create a company profile first.")
        return redirect(f'/accounts/create/')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect("job_list")   
    
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect("job_list")
    else:
        form = ApplicationForm()
    return render(request, "jobs/apply.html", {"form": form, "job": job})
    
    
@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related("job")
    return render(request, "jobs/my_application.html", {"applications": applications})

@login_required
def employer_applications(request):
    applications = Application.objects.filter(job__company__owner=request.user)
    return render(request, "jobs/employer_applications.html", {"applications": applications})


@login_required
def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__company__owner=request.user)
    application.status = "accepted"
    application.save()
    return redirect("employer_applications")


@login_required
def decline_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__company__owner=request.user)
    application.status = "declined"
    application.save()
    application.delete()
    return redirect("employer_applications")



@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()
    context =  {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form
    }
    return render(request, 'jobs/feed.html', context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'jobs/create_post.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('feed')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = Like.objects.filter(post=post, user=request.user)
    if liked.exists():
        liked.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect('feed')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('feed')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return redirect('feed')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect("feed")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("feed")

    return redirect("feed")
