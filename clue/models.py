from django.utils import timezone
from django.db import models
class crimeclue(models.Model):
    username = models.CharField(max_length=50) 
    password = models.CharField(max_length=50)
class Teacher(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

from django.db import models

class CrimeReport(models.Model):
    # Define status choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified as Real', 'Verified as Real'),
        ('Verified as Fake', 'Verified as Fake'),
        ('Forwarded to Principal', 'Forwarded to Principal'),
        ('Counseling Approved', 'Counseling Approved'),
        ('Closed by Principal', 'Closed by Principal'),
        ('Warning', 'Warning'),
        ('Suspended', 'Suspended'),
        ('Dismissed', 'Dismissed'),
    ]
    
    date = models.DateTimeField()
    category = models.CharField(max_length=255)
    comment = models.TextField()
    year = models.CharField(max_length=10, null=False, default='Unknown')
    location = models.CharField(max_length=255, null=False, default='Unknown')
    reported_by = models.CharField(max_length=255, default="Unknown")
    proof = models.FileField(upload_to='proofs/', null=True, blank=True)
    
    # Use choices for status
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    forwarded_to_principal = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Crime Report {self.id} - {self.category}"


class Crime(models.Model):
    crime = models.OneToOneField(CrimeReport, on_delete=models.CASCADE, related_name="investigation_report")
    investigation_report = models.TextField(null=False)
    principal_action = models.CharField(max_length=50, null=True, blank=True)
    principal_action_text = models.TextField(null=True, blank=True)
    culprit_name = models.CharField(max_length=255, null=True, blank=True)  # Add culprit's name
    culprit_class = models.CharField(max_length=50, null=True, blank=True)  # Add culprit's class
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investigation Report for Crime ID {self.crime.id}"



from django.contrib.auth.hashers import make_password

class Psychologist(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased length to accommodate hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password before saving if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username




from django.db import models

class Council_Report(models.Model):
    psychologist = models.ForeignKey('Psychologist', on_delete=models.CASCADE)
    crime = models.ForeignKey('CrimeReport', on_delete=models.CASCADE, related_name='council_reports')
    report_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.psychologist.username} for Crime {self.crime.id} on {self.created_at}"


import random

class studentlog(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone = models.BigIntegerField(default=100)
    names = models.CharField(max_length=50)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        self.otp = '{:06d}'.format(random.randint(0, 999999))
        self.otp_created_at = timezone.now()
        self.save()


from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField('studentlog', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username




class Investigator(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased length to accommodate hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password before saving if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


