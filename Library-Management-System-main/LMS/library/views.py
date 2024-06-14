from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import StudentsForm, BookForm, Book_IssueForm, Book_instanceForm
from .models import Students, Book, Book_Issue, BookInstance
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def add_new_student(request):
    if request.method == "POST":
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show_students')
    else:
        form = StudentsForm()
    return render(request, 'add_new_student.html', {'form': form})

def add_new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            book_instance = BookInstance(book=book)
            book_instance.save()
            return redirect('/view_books')
    else:
        form = BookForm()
        form_instance = Book_instanceForm()
        return render(request, 'add_new_book.html', {'form': form, "form_instance": form_instance})

def add_new_book_instance(request):
    if request.method == "POST":
        form = Book_instanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/view_books')

def add_book_issue(request):
    if request.method == "POST":
        form = Book_IssueForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            book_to_save = BookInstance.objects.get(id=form.book_instance.id)
            book_to_save.Is_borrowed = True
            book_to_save.save()
            form.save()
            form.save_m2m()
            return redirect('/view_books_issued')
    else:
        context = {'form': Book_IssueForm, "book": BookInstance.objects.filter(Is_borrowed=False)}
        return render(request, 'add_book_issue.html', context=context)

def view_students(request):
    students = Students.objects.order_by('-id')
    return render(request, 'view_students.html', {'students': students})

def view_books(request):
    books = BookInstance.objects.order_by('id')
    return render(request, 'view_books.html', {'books': books})

def books_list(request):
    books = Book.objects.filter(is_deleted=False)
    return render(request, 'books_list.html', {'books': books})

def view_bissue(request):
    issue = Book_Issue.objects.order_by('-id')
    return render(request, 'issue_records.html', {'issue': issue})

def edit_student_data(request, roll):
    try:
        if request.method == "POST":
            std = Students.objects.get(id=request.session['id'])    
            form = StudentsForm(request.POST, instance=std)
            if form.is_valid():
                form.save()
            del request.session['id']
            return redirect("/show_students")
        else:
            student_to_edit = Students.objects.get(roll_number=roll)
            student = StudentsForm(instance=student_to_edit)
            request.session["id"] = student_to_edit.id
            return render(request, 'edit_student_data.html', {'student': student})
    except Exception as error:
        print(f"{error} occured at edit_student_data view")


def edit_book(request, id):
    # Your view logic goes here
    return render(request, 'edit_book.html') 

def edit_book_data(request, id):
    # Your view logic goes here
    return render(request, 'edit_book_data.html') 



def delete_student(request, roll):
    student = get_object_or_404(Students, roll_number=roll)
    if request.method == 'POST':
        student.delete()
        return redirect('/show_students')
    return render(request, 'confirm_student_delete.html', {'student': student})


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('view_books')
    return render(request, 'confirm_book_delete.html', {'book': book})

def return_issued_book(request, id):   
    obj = get_object_or_404(Book_Issue, id=id)
    return render(request, 'return_issued_book.html', {'obj': obj})
def edit_issued(request, id):
    obj = Book_Issue.objects.get(id=id)
    return HttpResponse(f"<h2>Edit Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be edited..</label><h2>The feature is coming soon</h2>")
