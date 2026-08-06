# apps/core/management/commands/populate_data.py
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from apps.companies.models import Company
from apps.jobs.models import Job
from apps.applications.models import Application

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample job board data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users', type=int, default=20,
            help='Number of users to create (default: 20)'
        )
        parser.add_argument(
            '--companies', type=int, default=10,
            help='Number of companies to create (default: 10)'
        )
        parser.add_argument(
            '--jobs', type=int, default=50,
            help='Number of jobs to create (default: 50)'
        )
        parser.add_argument(
            '--applications', type=int, default=100,
            help='Number of applications to create (default: 100)'
        )
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete existing data before populating'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting data population...'))
        
        if options['flush']:
            self.flush_data()
        
        # Create data in dependency order
        users = self.create_users(options['users'])
        companies = self.create_companies(users, options['companies'])
        jobs = self.create_jobs(companies, users, options['jobs'])
        applications = self.create_applications(jobs, users, options['applications'])
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Successfully created:'
            f'\n   • {len(users)} Users'
            f'\n   • {len(companies)} Companies'
            f'\n   • {len(jobs)} Jobs'
            f'\n   • {len(applications)} Applications'
        ))

    def flush_data(self):
        """Delete all existing data"""
        self.stdout.write(self.style.WARNING('⚠️  Flushing existing data...'))
        Application.objects.all().delete()
        Job.objects.all().delete()
        Company.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('   Data flushed successfully'))

    # =========================================================================
    # SAMPLE DATA
    # =========================================================================
    
    FIRST_NAMES = [
        'James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
        'David', 'Elizabeth', 'William', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Emma', 'Olivia',
        'Ava', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn'
    ]
    
    LAST_NAMES = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker'
    ]
    
    COMPANY_NAMES = [
        'TechNova Solutions', 'DataPulse Analytics', 'CloudBridge Systems', 'QuantumLeap AI',
        'PixelForge Studios', 'CyberShield Security', 'GreenLeaf Innovations', 'StellarSoft',
        'NexGen Robotics', 'BlueWave Media', 'RedStone Technologies', 'SilverLinx Networks',
        'GoldenPath Consulting', 'IronClad DevOps', 'SwiftStream Logistics', 'BrightMind AI',
        'DeepDive Research', 'EchoWave Communications', 'FusionCore Labs', 'Horizon Ventures'
    ]
    
    INDUSTRIES = [
        'Software Development', 'Artificial Intelligence', 'Cybersecurity', 'Data Analytics',
        'Cloud Computing', 'E-commerce', 'FinTech', 'HealthTech', 'EdTech', 'Gaming',
        'SaaS', 'Mobile Development', 'Web Development', 'DevOps', 'Blockchain',
        'IoT', 'Machine Learning', 'UX/UI Design', 'Digital Marketing', 'IT Consulting'
    ]
    
    JOB_TITLES = [
        'Senior Python Developer', 'Full Stack Engineer', 'DevOps Engineer', 'Data Scientist',
        'Frontend React Developer', 'Backend Engineer', 'Machine Learning Engineer',
        'Cloud Architect', 'Product Manager', 'UX/UI Designer', 'QA Engineer',
        'Mobile App Developer', 'Security Engineer', 'Site Reliability Engineer',
        'Technical Lead', 'Engineering Manager', 'Data Engineer', 'AI Research Scientist',
        'Blockchain Developer', 'Systems Administrator', 'Scrum Master', 'Business Analyst',
        'Technical Writer', 'Sales Engineer', 'Customer Success Manager'
    ]
    
    JOB_DESCRIPTIONS = [
        """We are seeking a talented {title} to join our growing team. 
        You will be responsible for designing, developing, and maintaining 
        scalable applications that serve millions of users worldwide. 
        The ideal candidate has a passion for clean code and innovative solutions.""",
        
        """Join our innovative team as a {title}! You'll work on cutting-edge 
        projects using the latest technologies. We value creativity, collaboration, 
        and a drive to push boundaries. This is an exciting opportunity to make 
        a real impact in a fast-paced environment.""",
        
        """Are you passionate about {field}? We're looking for a skilled {title} 
        to help us build the next generation of products. You'll collaborate 
        with cross-functional teams to deliver exceptional user experiences 
        and robust backend systems.""",
        
        """We're hiring a {title} to lead our technical initiatives. 
        In this role, you'll architect solutions, mentor junior developers, 
        and drive engineering excellence. If you thrive in dynamic environments 
        and love solving complex problems, we want to hear from you!"""
    ]
    
    REQUIREMENTS_TEMPLATES = [
        """• Bachelor's degree in Computer Science or related field
• 3+ years of experience in {field}
• Strong proficiency in {skill1} and {skill2}
• Experience with {skill3}
• Excellent problem-solving and communication skills
• Ability to work in a fast-paced, agile environment""",
        
        """• Proven experience as a {title}
• Expert knowledge of {skill1}
• Familiarity with {skill2} and {skill3}
• Strong understanding of software design patterns
• Experience with cloud platforms (AWS/Azure/GCP)
• Team player with excellent collaboration skills"""
    ]
    
    RESPONSIBILITIES_TEMPLATES = [
        """• Design and implement scalable {field} solutions
• Collaborate with product managers and designers
• Write clean, maintainable, and well-tested code
• Participate in code reviews and technical discussions
• Optimize application performance and reliability
• Mentor junior team members and share knowledge""",
        
        """• Develop and maintain core platform features
• Troubleshoot and debug production issues
• Contribute to architectural decisions
• Implement CI/CD pipelines and automation
• Monitor system health and performance metrics
• Stay up-to-date with emerging technologies"""
    ]
    
    BENEFITS = [
        """• Competitive salary and equity package
• Comprehensive health, dental, and vision insurance
• Flexible PTO and remote work options
• Professional development budget
• Home office stipend
• 401(k) matching""",
        
        """• Competitive compensation
• Health and wellness programs
• Flexible working hours
• Learning and development opportunities
• Team retreats and social events
• Parental leave"""
    ]
    
    LOCATIONS = [
        'San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA',
        'Boston, MA', 'Chicago, IL', 'Denver, CO', 'Los Angeles, CA',
        'Remote', 'London, UK', 'Berlin, Germany', 'Toronto, Canada',
        'Dublin, Ireland', 'Amsterdam, Netherlands', 'Singapore'
    ]
    
    SKILLS_POOL = [
        'Python', 'Django', 'React', 'JavaScript', 'TypeScript', 'Node.js',
        'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes', 'AWS',
        'GCP', 'Azure', 'GraphQL', 'REST APIs', 'Celery', 'RabbitMQ',
        'Terraform', 'CI/CD', 'Machine Learning', 'TensorFlow', 'PyTorch',
        'Pandas', 'NumPy', 'Go', 'Rust', 'Java', 'Kotlin', 'Swift',
        'Flutter', 'React Native', 'Vue.js', 'Angular', 'HTML/CSS',
        'Sass', 'Tailwind CSS', 'Bootstrap', 'Git', 'GitHub Actions',
        'Jenkins', 'CircleCI', 'Prometheus', 'Grafana', 'ELK Stack'
    ]
    
    COVER_LETTERS = [
        """Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company}. 
With my background in {field} and passion for building scalable solutions, 
I believe I would be a valuable addition to your team.

In my previous roles, I have successfully {achievement}. I am particularly 
drawn to {company} because of your commitment to innovation and your 
impressive work in {area}.

I would welcome the opportunity to discuss how my skills and experience 
align with your needs. Thank you for considering my application.

Best regards,
{applicant_name}""",
        
        """Hello {company} Team,

I am writing to express my strong interest in the {job_title} role. 
As a {field} professional with {years} years of experience, I have 
developed expertise in {skills}.

What excites me most about this opportunity is {reason}. I am confident 
that my technical abilities and collaborative approach would make me 
a great fit for your team.

I look forward to the possibility of contributing to {company}'s continued success.

Sincerely,
{applicant_name}"""
    ]

    # =========================================================================
    # USER CREATION
    # =========================================================================
    
    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'  Creating {count} users...')
        users = []
        
        # Create a superuser first
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            users.append(admin)
            self.stdout.write(f'    ✓ Created superuser: admin/admin123')
        
        for i in range(count):
            first_name = random.choice(self.FIRST_NAMES)
            last_name = random.choice(self.LAST_NAMES)
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"
            
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='demo1234',
                    first_name=first_name,
                    last_name=last_name
                )
                users.append(user)
            except IntegrityError:
                # Handle duplicate usernames
                continue
                
        self.stdout.write(f'    ✓ Created {len(users)} users')
        return users

    # =========================================================================
    # COMPANY CREATION
    # =========================================================================
    
    def create_companies(self, users, count):
        """Create sample companies"""
        self.stdout.write(f'  Creating {count} companies...')
        companies = []
        
        # Filter users who don't already own a company
        available_users = [u for u in users if not hasattr(u, 'company')]
        
        for i in range(min(count, len(available_users))):
            user = available_users[i]
            name = self.COMPANY_NAMES[i % len(self.COMPANY_NAMES)]
            
            # Make name unique if needed
            base_name = name
            counter = 1
            while Company.objects.filter(name=name).exists():
                name = f"{base_name} {counter}"
                counter += 1
            
            company = Company.objects.create(
                name=name,
                owner=user,
                description=self.generate_company_description(name),
                website=f"https://{slugify(name)}.com",
                email=f"careers@{slugify(name)}.com",
                phone=self.generate_phone(),
                industry=random.choice(self.INDUSTRIES),
                company_size=random.choice([c[0] for c in Company.SIZE_CHOICES]),
                founded_year=random.randint(2000, 2023),
                location=random.choice(self.LOCATIONS),
                address=f"{random.randint(100, 9999)} {random.choice(['Main St', 'Market St', 'Broadway', 'Park Ave'])}, {random.choice(self.LOCATIONS)}",
                is_verified=random.choice([True, False]),
                is_featured=random.choice([True, False, False, False]),  # 25% featured
                linkedin=f"https://linkedin.com/company/{slugify(name)}",
                twitter=f"https://twitter.com/{slugify(name)}",
                facebook=f"https://facebook.com/{slugify(name)}"
            )
            companies.append(company)
            
        self.stdout.write(f'    ✓ Created {len(companies)} companies')
        return companies

    def generate_company_description(self, company_name):
        descriptions = [
            f"{company_name} is a leading technology company specializing in innovative software solutions. "
            f"Founded with a vision to transform industries through cutting-edge technology, we have grown "
            f"into a team of passionate professionals dedicated to excellence.",
            
            f"At {company_name}, we believe in the power of technology to solve real-world problems. "
            f"Our diverse team of experts works tirelessly to deliver products that make a difference "
            f"in people's lives and businesses worldwide.",
            
            f"{company_name} is revolutionizing the way organizations approach digital transformation. "
            f"With our suite of powerful tools and services, we help clients navigate the complexities "
            f"of modern technology landscapes."
        ]
        return random.choice(descriptions)

    def generate_phone(self):
        return f"+1 ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"

    # =========================================================================
    # JOB CREATION
    # =========================================================================
    
    def create_jobs(self, companies, users, count):
        """Create sample jobs"""
        self.stdout.write(f'  Creating {count} jobs...')
        jobs = []
        
        if not companies:
            self.stdout.write(self.style.WARNING('    ⚠ No companies available to create jobs'))
            return jobs
        
        # Get users who can post jobs (not company owners, or allow all)
        available_posters = [u for u in users if hasattr(u, 'company') or random.choice([True, False])]
        if not available_posters:
            available_posters = users
        
        for i in range(count):
            company = random.choice(companies)
            poster = random.choice(available_posters)
            title = random.choice(self.JOB_TITLES)
            
            # Generate unique slug
            base_slug = slugify(f"{title}-{company.name}")
            slug = base_slug
            counter = 1
            while Job.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            job_type = random.choice([j[0] for j in Job.JOB_TYPES])
            experience = random.choice([e[0] for e in Job.EXPERIENCE_LEVELS])
            status = random.choice([s[0] for s in Job.STATUS_CHOICES])
            
            # Salary generation
            salary_min = random.choice([None, random.randint(40000, 80000)])
            salary_max = None
            if salary_min:
                salary_max = salary_min + random.randint(20000, 80000)
            
            # Expiration date (30-90 days from now)
            expires = timezone.now() + timedelta(days=random.randint(30, 90))
            
            # Generate content
            field = company.industry
            skills = random.sample(self.SKILLS_POOL, k=3)
            
            job = Job.objects.create(
                title=title,
                slug=slug,
                company=company,
                posted_by=poster,
                description=random.choice(self.JOB_DESCRIPTIONS).format(
                    title=title, field=field
                ),
                requirements=random.choice(self.REQUIREMENTS_TEMPLATES).format(
                    title=title, field=field, 
                    skill1=skills[0], skill2=skills[1], skill3=skills[2]
                ),
                responsibilities=random.choice(self.RESPONSIBILITIES_TEMPLATES).format(
                    field=field
                ),
                benefits=random.choice(self.BENEFITS) if random.choice([True, False]) else '',
                job_type=job_type,
                experience_level=experience,
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency='USD',
                location=random.choice(self.LOCATIONS),
                is_remote=random.choice([True, False, False]),  # 33% remote
                is_featured=random.choice([True, False, False, False, False]),  # 20% featured
                status=status,
                views_count=random.randint(0, 5000),
                applications_count=0,  # Will be updated
                expires_at=expires
            )
            jobs.append(job)
            
        self.stdout.write(f'    ✓ Created {len(jobs)} jobs')
        return jobs

    # =========================================================================
    # APPLICATION CREATION
    # =========================================================================
    
    def create_applications(self, jobs, users, count):
        """Create sample applications"""
        self.stdout.write(f'  Creating {count} applications...')
        applications = []
        
        if not jobs or not users:
            self.stdout.write(self.style.WARNING('    ⚠ Missing jobs or users for applications'))
            return applications
        
        # Get applicant users (not job posters ideally, but can be anyone)
        applicant_pool = [u for u in users if not u.is_superuser]
        if not applicant_pool:
            applicant_pool = users
        
        created_count = 0
        max_attempts = count * 3  # Prevent infinite loops
        attempts = 0
        
        while created_count < count and attempts < max_attempts:
            attempts += 1
            job = random.choice(jobs)
            applicant = random.choice(applicant_pool)
            
            # Skip if applicant is the job poster
            if job.posted_by == applicant:
                continue
            
            # Check for duplicate application
            if Application.objects.filter(job=job, applicant=applicant).exists():
                continue
            
            status = random.choice([s[0] for s in Application.STATUS_CHOICES])
            
            cover_letter = random.choice(self.COVER_LETTERS).format(
                job_title=job.title,
                company=job.company.name,
                field=job.company.industry,
                achievement="delivered high-impact projects on tight deadlines",
                area="innovative product development",
                years=random.randint(2, 8),
                skills=", ".join(random.sample(self.SKILLS_POOL, k=3)),
                reason="the opportunity to work with cutting-edge technology",
                applicant_name=f"{applicant.first_name} {applicant.last_name}"
            )
            
            try:
                application = Application.objects.create(
                    job=job,
                    applicant=applicant,
                    cover_letter=cover_letter,
                    portfolio_url=f"https://{slugify(applicant.username)}-portfolio.com" if random.choice([True, False]) else '',
                    linkedin_url=f"https://linkedin.com/in/{slugify(applicant.username)}" if random.choice([True, False]) else '',
                    expected_salary=random.choice([None, random.randint(50000, 150000)]),
                    notice_period=random.choice(['2 weeks', '1 month', '3 months', 'Immediate', '']),
                    status=status,
                    notes=random.choice([
                        '', '', '',  # 75% empty
                        'Strong candidate, recommend interview',
                        'Good background but missing some required skills',
                        'Excellent portfolio, fast-track to interview'
                    ])
                )
                applications.append(application)
                created_count += 1
                
                # Update job applications count
                job.applications_count = job.applications.filter().count()
                job.save(update_fields=['applications_count'])
                
            except IntegrityError:
                continue
                
        self.stdout.write(f'    ✓ Created {len(applications)} applications')
        return applications
