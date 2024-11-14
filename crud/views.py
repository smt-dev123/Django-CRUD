from django.shortcuts import render, redirect
from .models import Student
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    # Get the search query if exists
    search = request.GET.get('search_query', '')

    # Apply search filter if search query exists
    if search:
        students = Student.objects.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )
    else:
        students = Student.objects.all().order_by('-id')
    
    # Paginate the filtered or all students list
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    if request.method == "POST":
        if "add" in request.POST:
            name = request.POST.get('stName')
            email = request.POST.get('stEmail')
            try:
                Student.objects.create(name=name, email=email)
                messages.success(request, "Student added successfully.")
            except Exception as e:
                messages.error(request, f"Error adding student: {e}")
            return redirect('home')
        
        elif "update" in request.POST:
            get_id = request.POST.get('id')
            name = request.POST.get('stName')
            email = request.POST.get('stEmail')
            try:
                student = Student.objects.get(id=get_id)
                student.name = name
                student.email = email
                student.save()
                messages.success(request, "Student updated successfully.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
            except Exception as e:
                messages.error(request, f"Error updating student: {e}")
            return redirect('home')
        
        elif "delete" in request.POST:
            get_id = request.POST.get('id')
            try:
                student = Student.objects.get(id=get_id)
                student.delete()
                messages.success(request, "Student deleted successfully.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
            except Exception as e:
                messages.error(request, f"Error deleting student: {e}")
            return redirect('home')
    
    context = {
        "students": page_obj,
        "search": search
    }
    return render(request, 'main.html', context)