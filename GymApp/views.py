from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from GymApp.models import Contact,MembershipPlan,Trainer,Enrollment,Gallery,Attendance, Room, Topic, Message, VideoMeeting
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .Services import call_groq_api
import time
import os

# Create your views here.
def Home(request):
    return render(request,"index.html")

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"attendance.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')

        if not username or not email or not pass1 or not pass2:
            messages.error(request, "All fields are required.")
            return redirect('/signup')

        if len(username) < 3 or len(username) > 30:
            messages.info(request, "Username must be between 3 and 30 characters.")
            return redirect('/signup')

        if pass1 != pass2:
            messages.info(request, "Passwords do not match.")
            return redirect('/signup')

        if len(pass1) < 8:
            messages.warning(request, "Password must be at least 8 characters long.")
            return redirect('/signup')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return redirect('/signup')

        # Create user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.save()
        messages.success(request, "User created successfully. Please login.")
        return redirect('/login')

    return render(request, "signup.html")

def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        pass1 = request.POST.get('pass1', '')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username  # Get username from email
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('/login')

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('/login')

    return render(request, "handlelogin.html")


def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save()       
        messages.info(request,"Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
        
    return render(request,"contact.html")


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        trainer=request.POST.get('trainer')
        reference=request.POST.get('reference')
        address=request.POST.get('address')
        query=Enrollment(FullName=FullName,Email=email,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipplan=member,SelectTrainer=trainer,Reference=reference,Address=address)
        query.save()
        messages.success(request,"Thanks For Enrollment")
        return redirect('/join')



    return render(request,"enroll.html",context)

def allworkout(request):
    return render(request, "Allworkout.html")

def bicepsplan(request,level):
    workout_plans = {
        'beginner': ['Barbell Curls - 3 sets of 10 reps', 'Hammer Curls - 3 sets of 12 reps', 'Tricep Pushdowns - 3 sets of 10 reps'],
        'intermediate': ['Preacher Curls - 4 sets of 8 reps', 'Incline Dumbbell Curls - 4 sets of 10 reps', 'Overhead Tricep Extension - 4 sets of 10 reps'],
        'extreme': ['EZ Bar Curls - 5 sets of 6 reps', 'Concentration Curls - 5 sets of 8 reps', 'Skull Crushers - 5 sets of 8 reps']
    }
    
    plan = workout_plans.get(level, [])
    return render(request, 'bicepsandtriceps.html', {'level': level, 'plan': plan})

@login_required
def chatRoom(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    messages = room.messages.all().order_by('timestamp')

    if request.method == "POST":
        # Handle Message
        message_content = request.POST.get('message')
        if message_content:
            Message.objects.create(
                room=room,
                user=request.user,  # Assign the logged-in user
                content=message_content,
                timestamp=timezone.now()
            )
            return redirect('chatroom', room_name=room_name)  # Redirect to prevent form resubmission

        # Handle GIF Upload (if needed)
        gif = request.FILES.get('gif')
        if gif:
            Message.objects.create(
                room=room,
                user=request.user,
                content=f"Shared a GIF: {gif.name}",
                timestamp=timezone.now()
            )
            # Save the GIF logic here if necessary (you can use FileField in your model)

    return render(request, 'chatroom.html', {
        'room': room,
        'messages': messages
    })

@login_required
def createRoom(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            Room.objects.get_or_create(name=room_name)
            return redirect('chatroom', room_name=room_name)
    return render(request, 'createroom.html')

def chat_with_groq(request):
    if request.method == "POST":
        user_query = request.POST.get("question")  # Get the query from the form
        result = call_groq_api(user_query)  # Call Groq API
        
        if "error" in result:
            content = result["error"]
        else:
            content = result['choices'][0]['message']['content']
        
        return render(request, 'groq_ai_query.html', {'content': content})

    # Handle GET request by rendering the empty form
    return render(request, 'groq_ai_query.html', {'content': ''})

def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.username})

def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.username})

def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')

def logout_view(request):
    logout(request)
    return redirect("/login")

