from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CO, PO, COPOMapping, COAttainment, StudentMark
from django.contrib.auth.models import User
from openpyxl import load_workbook

# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'home.html', {'message': 'Registration successful!'})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html', {
                'message': 'Login successful!',
                'user': user
            })
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login') 

def add_course(request):
    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        user_id = request.POST.get('user')  # 👈 get from form

        try:
            user = User.objects.get(id=user_id)
            Course.objects.create(
                code=course_code,
                name=course_name,
                user=user  # ✅ set user from form
            )
            return redirect('add_course')  # or show success page
        except User.DoesNotExist:
            return render(request, 'add_course.html', {
                'error': 'Invalid user selected.'
            })

    users = User.objects.all()
    return render(request, 'add_course.html', {
        'users': users,
        'user': request.user
    })


def courses(request):
    if request.user.is_authenticated:
        courses = Course.objects.filter(user=request.user)
        return render(request, 'courses.html', {'courses': courses})
    else:
        return redirect('login')  # Redirect to login if not authenticated
    
@login_required
def add_co(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        co_number = request.POST.get('co_number')
        co_description = request.POST.get('description')
        max_marks = request.POST.get('max_marks')  # <-- get from form

        try:
            course = Course.objects.get(id=course_id, user=request.user)

            if CO.objects.filter(course=course, number=co_number).exists():
                messages.warning(request, "This CO already exists for the selected course.")
            else:
                CO.objects.create(
                    course=course,
                    number=co_number,
                    description=co_description,
                    max_score=max_marks  # <-- save to db
                )
                messages.success(request, "Course Outcome added successfully!")
            return redirect('add_co')

        except Course.DoesNotExist:
            messages.error(request, "Invalid course selected.")

    courses = Course.objects.filter(user=request.user)
    return render(request, 'add_co.html', {'courses': courses})

def add_po(request):
    if request.method == 'POST':
        po_number = request.POST.get('po_number')
        po_description = request.POST.get('po_description')

        PO.objects.create(
            number=po_number,
            description=po_description
        )
        return redirect('add_po')  # or show success page

    return render(request, 'add_po.html')


def add_mapping(request):
    if request.method == 'POST':
        co_id = request.POST.get('co')
        po_id = request.POST.get('po')
        level = request.POST.get('level')

        try:
            co = CO.objects.get(id=co_id)
            po = PO.objects.get(id=po_id)

            COPOMapping.objects.create(
                co=co,
                po=po,
                level=level
            )
            messages.success(request, "CO-PO mapping added successfully!")
            return redirect('add_mapping')

        except (CO.DoesNotExist, PO.DoesNotExist):
            messages.error(request, "Invalid CO or PO selected.")

    cos = CO.objects.filter(course__user=request.user)
    pos = PO.objects.all()
    courses = Course.objects.filter(user=request.user)
    return render(request, 'mapping.html', {'cos': cos, 'pos': pos, 'courses': courses})


def upload_marks(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        course_id = request.POST.get('course_id')

        try:
            course = Course.objects.get(id=course_id)
            # Normalize CO numbers for consistent matching
            cos = {co.number.strip().upper(): co for co in CO.objects.filter(course=course)}
        except Course.DoesNotExist:
            messages.error(request, "Invalid course selected.")
            return redirect('upload_marks')

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active
            header = [str(cell.value).strip().upper() for cell in sheet[1]]
            co_headers = header[2:]  # Skip Roll No and Name
        except Exception as e:
            messages.error(request, f"Failed to read Excel file: {e}")
            return redirect('upload_marks')

        created_count = 0
        updated_count = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or row[0] is None:
                continue  # Skip empty rows

            roll_no, name, *marks = row
            if not roll_no or not name:
                continue

            for i, co_name in enumerate(co_headers):
                co = cos.get(co_name.strip().upper())
                if co and i < len(marks) and marks[i] is not None:
                    obj, created = StudentMark.objects.update_or_create(
                        course=course,
                        co=co,
                        roll_number=str(roll_no).strip(),
                        defaults={
                            'student_name': str(name).strip(),
                            'obtained_marks': float(marks[i]),
                            'total_marks': 100
                        }
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        messages.success(request, f"{created_count} records created, {updated_count} updated successfully.")
        return redirect('upload_marks')

    return render(request, 'upload_marks.html', {'courses': courses})
   
def co_attainment_view(request):
    selected_course_id = request.GET.get('course_id')
    courses = Course.objects.filter(user=request.user)
    attainment_data = []
    selected_course = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        cos = CO.objects.filter(course=selected_course)

        for co in cos:
            marks = StudentMark.objects.filter(course=selected_course, co=co)
            total_obtained = sum(m.obtained_marks for m in marks)
            # Use co.max_score (or co.max_marks) for each student
            total_possible = marks.count() * float(getattr(co, 'max_score', getattr(co, 'max_marks', 0)))

            attainment_percent = 0
            if total_possible > 0:
                attainment_percent = round((total_obtained / total_possible) * 100, 2)

            # Save or update attainment in DB
            COAttainment.objects.update_or_create(
                course=selected_course,
                co=co,
                defaults={'attainment_percentage': attainment_percent}
            )

            attainment_data.append({
                'co_number': co.number,
                'co_description': co.description,
                'attainment': attainment_percent
            })

    return render(request, 'co_attainment.html', {
        'courses': courses,
        'selected_course': selected_course,
        'attainment_data': attainment_data
    })


def calculate_po_attainment(request):
    selected_course_id = request.GET.get('course_id')
    courses = Course.objects.filter(user=request.user)
    po_scores = {}
    selected_course = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        pos = PO.objects.all()
        cos = CO.objects.filter(course=selected_course)

        for po in pos:
            total_score = 0
            total_weight = 0

            for co in cos:
                try:
                    mapping = COPOMapping.objects.get(co=co, po=po)
                    attainment = COAttainment.objects.get(co=co, course=selected_course).attainment_percentage
                    total_score += attainment * mapping.level
                    total_weight += mapping.level
                except (COPOMapping.DoesNotExist, COAttainment.DoesNotExist):
                    continue

            po_scores[po.number] = round(total_score / total_weight, 2) if total_weight else 0

    return render(request, 'po_attainment.html', {
        'courses': courses,
        'selected_course': selected_course,
        'po_scores': po_scores
    })
