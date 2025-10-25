from django.template.loader import get_template
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from .models import CrimeReport, crimeclue, Teacher
from .forms import TeacherRegistrationForm
from django import template

CSRF_TRUSTED_ORIGINS = [
    "https://crimeclue.onrender.com",
]


from django.core.mail import send_mail
from django.template.loader import get_template 
def home(request):
    return render(request, "clue/home.html")

from django.shortcuts import render
from .models import CrimeReport

# clue/views.py


def add_user(request):
    crimeclue.objects.create(username='user', password='password')
    return HttpResponse("User added")







def pri_login(request):
    return render(request, "clue/principal/pri_login.html")


def cluelogin(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')
        try:
            login_obj = crimeclue.objects.filter(username=username).exists()
            if login_obj:
                user_obj = crimeclue.objects.get(username=username, password=password)
                request.session['USERNAME'] = user_obj.username

                # Fetch crime report data
                crime_reports = CrimeReport.objects.all()
                total_cases = crime_reports.count()
                solved_cases = crime_reports.filter(Q(status="Counseling Approved") | Q(status="Closed by Principal")).count()
                council = crime_reports.filter(status="Counseling Approved").count()
                dismissed_cases = crime_reports.filter(status="Dismissed").count()

                # Prepare context
                context = {
                    'crime_reports': crime_reports,
                    'total_cases': total_cases,
                    'council': council,
                    'solved_cases': solved_cases,
                    'dismissed_cases': dismissed_cases,
                }

                # Render the principal dashboard with the context
                return render(request, 'clue/principal/index.html', context)

            else:
                messages.error(request, "Invalid username or password.")
        except Exception as e:
            messages.error(request, "An error occurred during login. Please try again.")

    return render(request, 'clue/principal/pri_login.html')



def logout(request):
    del request.session['USERNAME']
    return render(request, "clue/principal/pri_login.html")

def investigator_logout(request):
    # Safely clear the session key
    if 'USERNAME' in request.session:
        del request.session['USERNAME']
    # Clear all session data
    logout(request)
    # Redirect to the login page
    return redirect('investigator')


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            teacher = Teacher.objects.get(username=username, password=password)
            request.session['USERNAME'] = teacher.username
            return redirect('teacher_home')
        except Teacher.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('teacher_login')
    return render(request, 'clue/tr_login.html')

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher registered successfully!')
            return redirect('principal_dashboard')
        else:
            messages.error(request, 'Error registering teacher. Please check the form.')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'clue/principal/register_teacher.html', {'form': form})

from .forms import PsychologistRegistrationForm

from django.contrib import messages
from django.shortcuts import render, redirect
from clue.forms import PsychologistRegistrationForm
from clue.models import Psychologist

def register_psychologist(request):
    if request.method == 'POST':
        form = PsychologistRegistrationForm(request.POST)
        if form.is_valid():
            # Ensure password is hashed before saving
            psychologist = form.save(commit=False)
            psychologist.password = make_password(form.cleaned_data['password'])  
            psychologist.save()
            messages.success(request, 'Psychologist registered successfully!')
            return redirect('principal_dashboard')
        else:
            messages.error(request, 'Error registering Psychologist. Please check the form.')
    else:
        form = PsychologistRegistrationForm()
    return render(request, 'clue/principal/register_psychologist.html', {'form': form})


from .forms import InvestigatorRegistrationForm
from .models import Investigator

def register_investigator(request):
    if request.method == 'POST':
        form = InvestigatorRegistrationForm(request.POST)
        if form.is_valid():
            # Ensure password is hashed before saving
            Investigator = form.save(commit=False)
            Investigator.password = make_password(form.cleaned_data['password'])  
            Investigator.save()
            messages.success(request, 'Investigator registered successfully!')
            return redirect('cluelogin')
        else:
            messages.error(request, 'Error registering Psychologist. Please check the form.')
    else:
        form = InvestigatorRegistrationForm()
    return render(request, 'clue/principal/register_investigator.html', {'form': form})


def teacher_home(request):
    username = request.session.get('USERNAME')
    print(f"Username from session: {username}")
    reports = CrimeReport.objects.filter(reported_by=username)
    print(f"Reports: {reports}")
    return render(request, 'clue/teacher_home.html', {'username': username, 'reports': reports})




from django.shortcuts import render, redirect

from django.contrib import messages



def is_principal(user):
    return user.groups.filter(name='Principal').exists()

# views.py
from django.shortcuts import render
def principal_decision(request, report_id):
    # Retrieve the crime report using the report_id
    report = get_object_or_404(CrimeReport, id=report_id)

    # If the form is submitted to update the status
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(CrimeReport.STATUS_CHOICES):  # Ensure the status is valid
            report.status = new_status
            report.save()

    context = {
        'report': report
    }

    return render(request, 'clue/decision/principal_decision.html', context)




def report_list(request):
    crime_reports = CrimeReport.objects.all()
    return render(request, 'clue/principal/index.html', {'crime_reports': crime_reports})


from django.shortcuts import render
from .models import CrimeReport

def investigate_table(request):
    investigate_reports = Crime.objects.all()
    return render(request, 'clue/principal/investigate.html', {'investigate':investigate_reports})



def approve_counseling(request, report_id):
    if request.method == "POST":
      
        crime_report = get_object_or_404(CrimeReport, id=report_id)
        crime_report.status = "Counseling Approved"
        crime_report.save()
        messages.success(request, "Counseling Approved Successfully!")
    return redirect('principal_dashboard')






def crime_detail(request):
    # Fetch all crime reports
    crime_reports = CrimeReport.objects.all()
    
    # Fetch all investigation reports

    investigation_reports = Crime.objects.all()
    
    return render(request, 'clue/principal/crime_detail.html', {
        'crime_reports': crime_reports,
        'investigation_reports': investigation_reports,
    })

# New: Investigator's status update view
def update_investigator_status(request, report_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status not in ["Verified as Real", "Verified as Fake"]:
            messages.error(request, "Invalid status update.")
            return redirect("investigator")

        report = get_object_or_404(CrimeReport, id=report_id)
        report.status = new_status
        if new_status == "Verified as Real":
            report.status = "Forwarded to Principal"
        report.save()
        messages.success(request, "Investigation status updated successfully!")
    return redirect("investigator")

from django.contrib.auth.decorators import login_required



def forward_to_principal(request, crime_id):
    crime = get_object_or_404(CrimeReport, id=crime_id)
    # Logic to mark the crime as forwarded to the principal
    crime.status = "Forwarded to Principal"
    crime.save()
    messages.success(request, "Crime report has been forwarded to the principal.")
    return redirect('/investigator/')



def review_report(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)

    if request.method == 'POST':
        # Update report status after investigation
        report.status = request.POST['status']
        report.save()
        return redirect('dashboard')

    return render(request, 'clue/decision/review_report.html', {'report': report})

# View for the Principal to take action on the crime report



from django.contrib import messages




# View for the Counselor to handle counseling and resolve the case

def counselor_handle(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)

    if request.method == 'POST':
        # Update report status after counseling is completed
        report.status = 'Resolved by Counselor'
        report.save()
        return redirect('dashboard')

    return render(request, 'clue/decision/counselor_handle.html', {'report': report})


from django.core.files.storage import FileSystemStorage

def upload_report(request):
    if request.method == "POST":
        # Retrieving form data
        date = request.POST["txtdate"]
        category = request.POST["txtselect"]
        comment = request.POST["txtcomment"]
        year = request.POST["txtyear"]
        location = request.POST["txtlocation"]
        username = request.session.get('USERNAME')
      
       
        proof = request.FILES.get("txtfile", None)
        fs = FileSystemStorage()
        if proof:
            filename = fs.save(str(proof), proof)

 
        crime_report = CrimeReport(
            date=date,
            category=category,
            comment=comment,
            year=year,
            location=location,
            reported_by=username, 
            proof=proof if proof else None
        )
        crime_report.save()

        messages.success(request, "Crime report submitted successfully.")
        return redirect('teacher_home') 

    return render(request, 'clue/upload_report.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def principal_dashboard(request):
    crime_reports = CrimeReport.objects.all()
    for report in crime_reports:
        print(report.id)  
    context = {'crime_reports': crime_reports}
    return render(request, 'clue/principal/index.html', context)



from .models import studentlog, Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import studentlog, Profile


def update_details(request):
    if request.method == 'POST':
        current_email = request.POST.get('current_email')
        new_email = request.POST.get('new_email')
        phone = request.POST.get('phone')
        profile_picture = request.FILES.get('profile_picture')  # Get the uploaded file

        # Fetch the studentlog user based on the current email
        user = studentlog.objects.filter(email=current_email).first()
        
        if user:
            # Only update if the new email is provided and it's different from the current email
            if new_email and new_email != current_email:
                # Check if the new email already exists in the database
                if studentlog.objects.filter(email=new_email).exists():
                    messages.error(request, 'The new email is already in use.')
                    return redirect('update_details')

                user.email = new_email  # Update the email address

            # Only update if the phone number is provided
            if phone:
                user.phone = phone  # Update the phone number

            # Save the user object after updating fields
            user.save()

            # Fetch the existing profile linked to this studentlog instance
            profile = Profile.objects.filter(student=user).first()  # Use `first()` to fetch the existing profile
            
            if profile:
            
                if profile_picture:
                    profile.profile_picture = profile_picture  # Update the profile picture
                    profile.save()
            else:
                # If no profile exists, create one
                profile = Profile.objects.create(student=user, profile_picture=profile_picture)

            # Success message after updating details
            messages.success(request, "🎉 Your details have been updated successfully! 🎉")
            
            return redirect('update_details')  # Redirect to the same page to display the message

        else:
            messages.error(request, 'User not found with the given email.')

    return render(request, 'clue/update_details.html')




def admins(request):
    return render(request, 'clue/admin/admins.html')




def get_status_badge_class(status):
    status_classes = {
        "Pending": "badge-warning",
        "Verified as Real": "badge-primary",
        "Verified as Fake": "badge-danger",
        "Counseling Approved": "badge-success",
        "Closed by Principal": "badge-dark",
    }
    return status_classes.get(status, "badge-info")  # Default to 'badge-info' for unknown statuses

def investigator(request):
    """Display a list of crimes to the investigator."""
    crimes = CrimeReport.objects.all()
    return render(request, 'clue/investigator.html', {'crimes': crimes})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CrimeReport, Crime, studentlog
from django.urls import reverse

def submit_report(request, crime_id):
    """Handle the submission of an investigation report by the investigator."""
    crime_report = get_object_or_404(CrimeReport, id=crime_id)

    # Correctly reference the Crime model via `investigation_details`
    crime_details, created = Crime.objects.get_or_create(crime=crime_report)

    if request.method == "POST":
        # Get data from the form
        report = request.POST.get('investigation_report')
        status = request.POST.get('status')

        # Update the CrimeReport's status (this is part of the CrimeReport model, not Crime)
        if status == 'Verified':
            crime_report.status = 'Verified as Real'
            culprit_name = request.POST.get('culprit_name')
            culprit_class = request.POST.get('culprit_class')
            if not report or not status or not culprit_name or not culprit_class:
                messages.error(request, "All fields (investigation report, status, culprit name, and culprit class) are required.")
                return redirect(reverse('submit_report', args=[crime_id]))

            # Save the investigation report and the culprit details in the Crime model
            crime_details.investigation_report = report
            crime_details.culprit_name = culprit_name
            crime_details.culprit_class = culprit_class
            crime_details.save()

        elif status == 'Fake':
            crime_report.status = 'Verified as Fake'
            if not report or not status:
                messages.error(request, "Investigation report and status are required.")
                return redirect(reverse('submit_report', args=[crime_id]))

            # Save the investigation report
            crime_details.investigation_report = report
            crime_details.save()

            # Suspend the student
            student = get_object_or_404(studentlog, email=crime_report.reported_by)
            student.status = 'Suspended'
            student.save()
            messages.success(request, 'The student has been suspended.')

        else:
            messages.error(request, "Invalid status provided.")
            return redirect(reverse('submit_report', args=[crime_id]))

        # Save the status update to the CrimeReport
        crime_report.save()

        messages.success(request, "Investigation report, status, and culprit details updated successfully.")
        return redirect('investigator')  # Redirect to the investigator dashboard or relevant page

    return render(request, 'clue/submit_invest.html', {'crime_report': crime_report, 'crime_details': crime_details})




def update_report_action(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    if request.method == "POST":
        # Update the report status or any other fields here
        report.status = "Approved"  # or any other action you'd like to perform
        report.save()
        return redirect('principal_dashboard')  # Redirect to the dashboard after action
    return render(request, 'clue/principal/decision.html', {'report': report})





def crime_report_list(request):
    # Fetch the crime reports
    crime_reports = CrimeReport.objects.all()
    
    # Render the template and pass the crime reports
    return render(request, 'clue/principal/index.html', {'crime_reports': crime_reports})






def crime_report_table(request):
    crime_reports = CrimeReport.objects.all()
    return render(request, 'clue/principal/crime_report_table.html', {'crime_reports': crime_reports})



from django.shortcuts import render, redirect, get_object_or_404


# Update Crime Report Status
def update_report_status(request, report_id):
    # Get the crime report by ID or return 404 if not found
    report = get_object_or_404(CrimeReport, id=report_id)

    if request.method == 'POST':
        # Get the new status from the form
        new_status = request.POST.get('status')

        # Update the report's status
        if new_status in ['Pending', 'Under Review', 'Counseling Approved']:
            report.status = new_status
            report.save()  # Save the updated status to the database
            return redirect('crime_reports')  # Redirect back to the list of crime reports
        else:
            # Handle invalid status
            return HttpResponse("Invalid status", status=400)

    # If the method is not POST, we return an error
    return HttpResponse("Invalid request method", status=405)


# views.py



from .models import CrimeReport, Crime, studentlog
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def principal_action(request, crime_id):
    # Fetch the CrimeReport and associated Crime instance
    crime_report = get_object_or_404(CrimeReport, id=crime_id)
    crime = get_object_or_404(Crime, crime=crime_report)

    if request.method == 'POST':
        # Get the principal's action and additional details
        principal_action = request.POST.get('principal_action')
        principal_action_text = request.POST.get('principal_action_text')

        # Update the Crime model with the principal's action
        crime.principal_action = principal_action
        crime.principal_action_text = principal_action_text
        crime.save()

        # Update the CrimeReport status and forward to principal if necessary
        crime_report.status = principal_action
        if principal_action == 'Suspended':
            crime_report.status = 'Suspended'
        elif principal_action == 'Warning':
            crime_report.status = 'Warning'

        elif principal_action == 'Dismissed':
            crime_report.status = 'Closed by Principal'
        crime_report.save()

        # Suspend the student if the status is "Fake"
        if principal_action == 'Verified as Fake':
            messages.success(request, 'The student has been suspended.')
            # Implement suspension logic here
            # For example, assuming 'reported_by' is the student's email in CrimeReport
            student = get_object_or_404(studentlog, email=crime_report.reported_by)
            student.status = 'Suspended'  # Ensure you have a status field in your Student model
            student.save()

        return redirect('crime_detail')  # Redirect to the relevant view after action submission

    return render(request, 'clue/principal/principal_action.html', {
        'crime_report': crime_report,
        'crime': crime,
    })







from django.shortcuts import render
from .models import Crime, CrimeReport

def crime_detail(request):
    # Fetch all Crime objects along with their related CrimeReport objects
    crimes = Crime.objects.exclude(crime__status='Verified as Fake')

    return render(request, 'clue/principal/crime_detail.html', {
        'crimes': crimes,
    
    
    })




from django.shortcuts import redirect
def psychologist_logout(request):
   
    if 'USERNAME' in request.session:
        del request.session['USERNAME']  
    request.session.flush() 
    
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to the login page
    return redirect('psychologist_login')


from .models import Psychologist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def psychologist_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Fetch psychologist object
            psychologist = get_object_or_404(Psychologist, username=username)
            
            # Check password securely
            if check_password(password, psychologist.password):
                # Save the psychologist's username in session
                request.session['USERNAME'] = psychologist.username
                return redirect('psychologist_dashboard')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Psychologist.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
        return redirect('psychologist_login')  # Reload the login page on error

    # Render the login page for GET requests
    return render(request, 'clue/counciler/psychologist_login.html')



from .models import Council_Report
from django.db.models import Q
from django.shortcuts import render

def psychologist_dashboard(request):
    username = request.session.get('USERNAME', None)
    if not username:
        return redirect('psychologist_login')

    # Query for assigned cases (modify query as needed)
    assigned_cases = CrimeReport.objects.filter(Q(status='Warning') | Q(status='Suspended'))


    return render(request, 'clue/counciler/psychologist_dashboard.html', {
        'username': username,
        'assigned_cases': assigned_cases,
    })



def council_report(request):
    psychologist_id = request.session.get('psychologist_id')
    if not psychologist_id:
        return redirect('psychologist_login')

    if request.method == 'POST':
        report_details = request.POST.get('report_details')
        psychologist = Psychologist.objects.get(id=psychologist_id)
        Council_Report.objects.create(psychologist=psychologist, report_details=report_details)
        messages.success(request, 'Council report updated successfully!')
        return redirect('psychologist_dashboard')

    return render(request, 'clue/counciler/council_report.html')


from django.shortcuts import render, redirect
from .models import CrimeReport, Psychologist, Council_Report


from django.shortcuts import render, redirect
from .models import Council_Report, CrimeReport, Psychologist






def counseling_report_page(request):
    # Retrieve counseling reports for the logged-in user
    reports = Council_Report.objects.filter(psychologist=request.user)
    return render(request, 'clue/counciler/counseling_report.html', {'reports': reports})




from django.shortcuts import render, get_object_or_404, redirect
from .models import CrimeReport, Council_Report, Psychologist

def submit_counseling_report(request, crime_id):
    # Assuming a direct link between the user and the psychologist, we get the first available Psychologist
    # If you have more than one, you need to associate the user with the correct psychologist
    try:
        # Get the first available psychologist (or change the logic to match your needs)
        psychologist = Psychologist.objects.first()
    except Psychologist.DoesNotExist:
        return redirect('error_page')  # Handle if no psychologists are found

    crime_report = get_object_or_404(CrimeReport, id=crime_id)

    if request.method == 'POST':
        # Get the report details from the form
        report_details = request.POST.get('report_details')

        # Create the council report
        Council_Report.objects.create(
            psychologist=psychologist,
            crime=crime_report,
            report_details=report_details,
        )

        # Redirect to a dashboard or success page
        return redirect('psychologist_dashboard')

    return render(request, 'clue/counciler/counseling_report.html', {
        'crime_report': crime_report,
    })







from django.shortcuts import render, redirect
from .models import CrimeReport, Council_Report

def counseling_and_crime_reports(request):
    # Fetch CrimeReports where forwarded_to_principal is True
    crime_reports = CrimeReport.objects.filter(
        forwarded_to_principal=True
    ).order_by('status')  # Ensure ordering, so 'Counseling Approved' is handled as needed

    # Handle "Approve Counseling" action when POST is made
    if request.method == "POST":
        crime_id = request.POST.get('crime_id')
        if crime_id:
            crime_report = CrimeReport.objects.get(id=crime_id)
            # Update the status of the crime report to 'Counseling Approved'
            crime_report.status = 'Counseling Approved'
            crime_report.save()
            return redirect('counseling_and_crime_reports')  # Redirect to the same page to refresh

    # Prepare list of crime reports with their associated council report details
    crime_reports_with_counseling_details = []
    for report in crime_reports:
        # Fetch the first related council report (if any)
        council_report = Council_Report.objects.filter(crime=report).first()
        
        # Add the counseling report details if exists
        if council_report:
            report.counseling_report_details = council_report.report_details
        else:
            report.counseling_report_details = None

        crime_reports_with_counseling_details.append(report)

    return render(request, 'clue/principal/counsel.html', {
        'crime_reports': crime_reports_with_counseling_details  # Pass the updated reports list
    })




def home_login(request):
    
    return render(request,'clue/home_login.html')


from .models import CrimeReport, studentlog

def view_student_reports(request, student_id):
    student = get_object_or_404(studentlog, id=student_id)
    
    # Fetch the crime reports where the student reported the crime
    reports = CrimeReport.objects.filter(reported_by=student.email)

    # Fetch the related investigation reports (Crime objects) that are linked to those reports
    investigate = Crime.objects.filter(crime__in=reports)

    context = {
        'student': student,
        'reports': reports,
        'investigate': investigate,
    }
    return render(request, 'clue/principal/view_student_reports.html', context)



from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, studentlog, CrimeReport
def stdlogin(request):
    template = loader.get_template('clue/stu_login.html')
    context = {}

    if request.method == "POST":
        name = request.POST.get('txtemail')
        password = request.POST.get('txtpassword')
        
        # Check if the email exists
        if studentlog.objects.filter(email=name).exists():
            # Verify the password
            user_obj = studentlog.objects.filter(email=name, password=password).first()
            if user_obj:
                # Check if any crime reported by the user is verified as fake
                if CrimeReport.objects.filter(reported_by=name, status='Verified as Fake').exists():
                    context = {"suspended_warning": "Your account is suspended due to fake reporting."}
                else:
                    # Store user email in session
                    request.session['USERNAME'] = user_obj.email

                    # Create or get a User object
                    user, created = User.objects.get_or_create(username=user_obj.email, defaults={'password': user_obj.password, 'email': user_obj.email})

                    # Check if profile already exists for this student
                    profile_instance = Profile.objects.filter(student=user_obj).first()
                    if not profile_instance:
                        # If profile doesn't exist, create it
                        profile_instance = Profile.objects.create(student=user_obj, user=user)

                    # Set default profile picture if not set
                    if not profile_instance.profile_picture:
                        profile_instance.profile_picture = 'profile_pics/profile.png'  # Default picture path
                        profile_instance.save()

                    # Pass profile and profile picture to context
                    context = {
                        'profile': user_obj,
                        'profile_picture': profile_instance.profile_picture.url if profile_instance.profile_picture else None,  # Ensure URL is passed
                    }

                    # Render the next page after login (e.g., student dashboard or profile)
                    template = loader.get_template('clue/aflogin.html')
                    return HttpResponse(template.render(context, request))
            else:
                context = {"error": "Invalid password"}
        else:
            context = {"error": "Invalid email"}
    
    return HttpResponse(template.render(context, request))







def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = studentlog.objects.filter(email=email).first()
        if user:
            user.generate_otp()
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {user.otp}',
                'admin@crimeclue.com',
                [user.email],
            )
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('password_reset_verify', email=email)
        else:
            messages.error(request, 'User with this email does not exist.')
    return render(request, 'clue/password_reset_request.html')


from django.utils import timezone

from django.contrib import messages


def password_reset_verify(request, email):
    user = studentlog.objects.filter(email=email).first()
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user and user.otp == otp and (timezone.now() - user.otp_created_at).total_seconds() < 300:
            if new_password == confirm_password:
                user.password = new_password
                user.otp = None
                user.otp_created_at = None
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('stdlogin')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Invalid OTP or OTP has expired.')
    return render(request, 'clue/password_reset_verify.html', {'email': email})


from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import studentlog



def register(request):
    return render(request,"clue/stu_reg.html")
def stdreg(request):
    if request.method=="POST":
        name=request.POST["txtname"]
        ph=request.POST["txtphone"]
        mail=request.POST["txtemail"]
        password=request.POST["txtpassword"]

        try:
            validate_email(mail)
        except ValidationError:
            return render(request,"clue/stu_reg.html",{"email_error":"invalid email address. "})
        if not ph.isdigit() or len(ph) != 10:
            return render (request,"clue/stu_reg.html",{"phone_error":"invalid phone number. "})
        try:
            std=studentlog(names=name,email=mail,phone=ph,password=password)
            std.save()
            return render(request,"clue/home_login.html")
        except IntegrityError:
            return render(request,"clue/stu_reg.html",{"name_error":"email or phone already exists."})
    return render(request,"clue/stu_reg.html")

def homepage(request):
    total_crimes_reported = CrimeReport.objects.count()
    total_students_logged_in = studentlog.objects.count()
    total_teachers_logged_in =Teacher.objects.count()
    total_cases_solved = CrimeReport.objects.filter(status__in=['Counseling Approved', 'Closed by Principal','Suspended','Dismissed','Verified as Fake']).count() 
    context = { 'total_crimes_reported': total_crimes_reported,
                'total_students_logged_in': total_students_logged_in,
                'total_cases_solved': total_cases_solved,
                 'total_teachers_logged_in':total_teachers_logged_in,
                   }

    return render(request,"clue/home.html",context)

from django.shortcuts import render
from .models import CrimeReport  # Replace with the actual name of your model

def user_reports(request):
    # Retrieve all reports submitted by the logged-in user
    user = request.user  # Assuming you have user authentication set up
    reports = CrimeReport.objects.filter(reported_by=user)  # Adjust this filter as needed
    
    # Pass the reports to the template
    context = {
        'reports': reports,
    }
    return render(request, 'clue/stu_home.html', context)


def view_reports(request):
    username = request.session.get('USERNAME')
    if not username:
        return redirect('stdlogin')  # Redirect to login if user isn't authenticated

    reports = CrimeReport.objects.filter(reported_by=username)
    return render(request, 'clue/reports.html', {'reports': reports})






def investigator_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Fetch investigator object
            investigator = get_object_or_404(Investigator, username=username)
            
            # Check password securely
            if check_password(password, investigator.password):
                # Save the investigator's username in the session
                request.session['USERNAME'] = investigator.username
                return redirect('investigator')  # Redirect to the investigator's dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Investigator.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
        
        # Reload the login page on error
        return redirect('Investigator_login')

    # Render the login page for GET requests
    return render(request, 'clue/investigator/invest.html')



# Delete Crime Report View
def delete_crime_report(request, crime_id):
    crime_report = get_object_or_404(CrimeReport, id=crime_id)
    
    # Delete the associated crime report and the related crime
    crime_report.delete()
    
    # Redirect to the crime report list or some other page
    return redirect('crime_detail')  # Replace 'crime_report_list' with your URL name


def confirm_delete_crime_report(request, crime_id):
    crime_report = get_object_or_404(CrimeReport, id=crime_id)
    if request.method == "POST":
        # Delete the associated crime report and the related crime
        crime_report.delete()
        return redirect('crime_report_list')  # Replace with your list page URL
    return render(request, 'clue/principal/confirm_delete.html', {'crime_report': crime_report})


# View to show all students and allow deletion
def student_list(request):
    students = studentlog.objects.all()  # Get all students
    return render(request, 'clue/principal/student_list.html', {'students': students})

# View to delete a student
def delete_student(request, student_id):
    student = studentlog.objects.get(id=student_id)
    student.delete()  # Delete the student
    return redirect('student_list')  # Redirect back to the student list page
