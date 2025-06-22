from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import Course, CO, PO, COPOMapping, COAttainment
# Create your views here.
def index(request):

    return render(request, "calculator/index.html")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    
    return render(request, 'calculator/register.html',{
        'form':form,
    })
         


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Change 'home' to your desired redirect URL name
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'calculator/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Change 'login' to your desired redirect URL name


def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        user = request.user
        if course_name and course_code:
            course = Course(name=course_name, course_code=course_code, user=user)
            course.save()
            messages.success(request, 'Course added successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'calculator/add_course.html')

def add_cos(request):
    if request.method == 'POST':
        co_number = request.POST.get('co_number')  # Updated field name
        co_description = request.POST.get('co_description')  # New field for description
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, 'Selected course does not exist.')
            return redirect('add_cos')
        if co_number and co_description:
            co = CO(number=co_number, course=course, description=co_description)
            co.save()
            messages.success(request, 'CO added successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all fields.')
    courses = Course.objects.filter(user=request.user)
    return render(request, 'calculator/add_cos.html', {'courses': courses})

def add_pos(request):
    if request.method == 'POST':
        po_number = request.POST.get('pos_name')
        co_id = request.POST.get('cos_id')
        co = CO.objects.get(id=co_id)
        if po_number and co:
            po = PO(number=po_number, description='')
            po.save()
            messages.success(request, 'PO added successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all fields.')
    co_list = CO.objects.filter(course__user=request.user)
    return render(request, 'calculator/add_pos.html', {'cos_list': co_list})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'calculator/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    co_list = CO.objects.filter(course=course)
    for co in co_list:
        co.pos_list = [mapping.po for mapping in COPOMapping.objects.filter(co=co)]
    return render(request, 'calculator/course_detail.html', {
        'course': course,
        'cos_list': co_list,
    })

def calculate_po_attainment(request, course_id):
    course = Course.objects.get(id=course_id)
    pos = PO.objects.all()
    cos = CO.objects.filter(course=course)

    po_scores = {}

    for po in pos:
        total_score = 0
        total_weight = 0
        for co in cos:
            try:
                mapping = COPOMapping.objects.get(co=co, po=po)
                attainment = COAttainment.objects.get(co=co).attainment_percentage
                total_score += attainment * mapping.level
                total_weight += mapping.level
            except (COPOMapping.DoesNotExist, COAttainment.DoesNotExist):
                continue
        po_scores[po.number] = round(total_score / total_weight, 2) if total_weight else 0

    return render(request, 'calculator/po_attainment.html', {
        'course': course,
        'po_scores': po_scores
    })

def enter_matrix(request, course_id):
    course = Course.objects.get(id=course_id)
    cos = CO.objects.filter(course=course)
    pos = PO.objects.all()
    if request.method == 'POST':
        for co in cos:
            for po in pos:
                level = request.POST.get(f"matrix_{co.id}_{po.id}")
                if level:
                    COPOMapping.objects.update_or_create(
                        co=co, po=po,
                        defaults={'level': int(level)}
                    )
        messages.success(request, 'CO-PO matrix saved successfully!')
        return redirect('course_detail', course_id=course.id)
    return render(request, 'calculator/enter_matrix.html', {'course': course, 'cos': cos, 'pos': pos})