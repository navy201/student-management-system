from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse


@login_required(login_url='login')
def home(request):
    query = request.GET.get('search')

    students = Student.objects.all()

    if query:
        query = query.strip()
        if query != "":
            students = Student.objects.filter(
                name__icontains=query
            ) | Student.objects.filter(
                course__icontains=query
            )

    return render(request, "home.html", {
    "students": Student.objects.all().order_by('-id')[:5],
    "total_students": Student.objects.count()
})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('students')
    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    return render(request, "student_edit.html", {"form": form})


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('students')

    return render(request, "delete_student.html", {"student": student})




def student_details(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "student_details.html", {"student": student})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
def students(request):
    query = request.GET.get('search')

    student_list = Student.objects.all().order_by('id')
    if query:
        student_list = student_list.filter(name__icontains=query)

    paginator = Paginator(student_list, 5)  # Show 5 students per page

    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    return render(request, "students.html", {
        "students": students,
        "total_students": student_list.count()
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username, password=password)

        print("User:", user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Course', 'Email'])

    students = Student.objects.all()

    for student in students:
        writer.writerow([
            student.name,
            student.age,
            student.course,
            student.email,
        ])

    return response