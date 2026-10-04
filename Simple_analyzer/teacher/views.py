from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import CreateAccountForm,StudentAddForm,AddMarksForm,MarkFormSet,SetChoicesForm,CustomLoginForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .models import Student,Stream,Marks,Subject
from django.forms import modelformset_factory



# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form=CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)

            if user is not None:
               login(request,user)
               return redirect(reverse('dashboard'))
        else:
             return render(request,'user/login.html',{
                                "form":form,
                                          
                                })
           
       
    else:
        form=CustomLoginForm()
        return render(request,'user/login.html',{
            "form":form
        })

    


def dashboard_view(request):
    streams=Stream.objects.all()
    if request.method=='POST':
            stream_id=request.POST.get("stream")
            
            return redirect('students',stream_id=stream_id)
    return render(request,'user/dashboard.html',{
        "streams":streams
    })
def signup_view(request):
    if request.method == 'POST':
        form= CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
    else:
        form=CreateAccountForm()
        return render(request,'user/signup.html',{
            "form":form
        })

def home(request):
    return render(request, "user/home.html")

def view_students(request,stream_id):
    stream=Stream.objects.get(id=stream_id)
    learners=stream.students.all()
    total_students=len(learners)
    if request.method == 'POST':
        id=request.POST.get("stream")
        return redirect('addstudent',stream_id=id)
    
    return render(request,"user/students.html",{
        "learners":learners,
        "stream":stream,
        "total_students":total_students
    })
def add_student(request,stream_id):
    stream=get_object_or_404(Stream,id=stream_id)
    if request.method == 'POST':
        form=StudentAddForm(request.POST)
        if form.is_valid():
            student=form.save(commit=False)
            student.stream=stream
            student.save()
            return redirect('students',stream_id)
        
    else:
        form = StudentAddForm()
    return render(request,'user/addStudent.html',{
            "form":form
        })

def select_stream(request):
    streams=Stream.objects.all()
    if request.method == 'POST':
        stream_id=request.POST.get("stream")
        stream=get_object_or_404(Stream,id=stream_id)
        return redirect('addmarks',stream_id)
    return render(request,'user/selectstream.html',{
        "streams":streams
    })

def add_marks(request,stream):
    students=Student.objects.filter(stream=stream)
    subjects=Subject.objects.all()
    
    
    if request.method == 'POST':
        for student in students:
           score=request.POST.get(f'mark_{student.id}')
           exam_term=request.POST.get("exam_term")
           subject_id=request.POST.get('subject_id')
           subject=get_object_or_404(Subject,id=subject_id)
           if score:
               Marks.objects.update_or_create(
                   student=student,
                   subject=subject,
                   exam_term=exam_term,
                   defaults={
                       'score':score
                   }
               )
        return redirect('dashboard')

    return render(request,'user/addmarks.html',{
              "students":students,
              "subjects":subjects,
              "exam_terms":Marks.TermChoices.choices,
              

            
            
        })


    


def view_marks(request):
    subjects=Subject.objects.all()
    streams=Stream.objects.all()
    if request.method == 'POST':
        stream_id=request.POST.get('stream')
        subject_id=request.POST.get("subject")
        exam_term=request.POST.get("exam_term")
        return redirect("showmarks",stream_id,subject_id,exam_term)
    return render(request,'user/viewmarks.html',{
        "subjects":subjects,
        "streams":streams,
        "exam_terms":Marks.TermChoices.choices
    })

def show_marks(request,stream_id,subject_id,exam_term):


    subject=Subject.objects.get(id=subject_id)
    stream=Stream.objects.get(id=stream_id)
    students=Student.objects.filter(stream=stream)
    exam_term=exam_term

    
    

    results=[Marks.objects.filter(student=student ,subject=subject,exam_term=exam_term).first() for student in students ]
              
   
    return render(request,"user/showmarks.html",{
        "students":students,
        "results":results,
        
    })

def generate_view(request):
    streams=Stream.objects.all()
    terms=Marks.TermChoices.choices
    if request.method == 'POST':
        stream_id=request.POST.get("stream")
        term=request.POST.get("term")
        return redirect('compute_marks',stream_id,term)
    return render(request,"user/generatereport.html",{
        "streams":streams,
        "terms":terms
    })

def compute_marks(request,stream_id,term):
    stream=Stream.objects.get(id=stream_id)
    students=Student.objects.filter(stream=stream)
    exam_term=term
    subjects=Subject.objects.all()
    results = []
    student_totals=[]
    def get_rank(values,number):
        ranked=sorted(values,reverse=True)
        return ranked.index(number)+1

    for student in students:
           marks = {}

           total = 0
           

           for subject in subjects:
              mark = Marks.objects.filter(
              student=student,
              subject=subject,
              exam_term=exam_term
              ).first()
              
              
              
              marks[subject.subject_code]=mark
              if mark:
                total+=mark.score
           student_totals.append(
                          total
                      )
           try:
                   totalmarks={name:mark for name ,mark in marks.items() if mark!=None}
                   initial_mean=total/len(totalmarks)
                   mean=round(initial_mean,2)
           except ZeroDivisionError:
                  mean=""
          
           results.append({
                "student": student,
                "marks": marks,
                "total": total,
                "mean":mean
                
              })
    for result in results:
        rank=get_rank(student_totals,result["total"])
        result["rank"]=rank
          
           
    
    return render(request,"user/finalreport.html",{
            "results":results,
            "subjects":subjects,
            "rank":rank
            
        })

    