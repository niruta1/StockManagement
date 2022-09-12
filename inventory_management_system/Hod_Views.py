from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from inventory.models import Department, Location, Purpose, Category, Item, CustomUser, Staff, StaffLeave, \
    StaffFeedback, ItemRequest, Medicine
from django.contrib import messages
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now


@login_required(login_url='/')
def HOME(request):
    item_count = Item.objects.all().count()
    department_count = Department.objects.all().count()
    location_count = Location.objects.all().count()
    medicine = Medicine.objects.all()
    expiring_meds =[]
    for med in medicine:
        if med.get_remaining_days < 10:
            expiring_meds.append(med)

    

    context = {
        'item_count': item_count,
        'department_count': department_count,
        'location_count': location_count,
        'expiring_medicine':expiring_meds

    }

    return render(request, 'Hod/home.html', context)


@login_required(login_url='/')
def ADD_ITEMS(request):
    department = Department.objects.all()
    location = Location.objects.all()
    purpose = Purpose.objects.all()
    category = Category.objects.all()

    if request.method == "POST":
        item_pic = request.FILES.get('item_pic')
        item_name = request.POST.get('item_name')
        specification = request.POST.get('specification')
        quantity = request.POST.get('quantity')
        total_amount = request.POST.get('total_amount')
        category_id = request.POST.get('category_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        department_id = request.POST.get('department_id')
        location_id = request.POST.get('location_id')
        purpose_id = request.POST.get('purpose_id')

        department = Department.objects.get(id=department_id)
        location = Location.objects.get(id=location_id)
        purpose = Purpose.objects.get(id=purpose_id)
        category = Category.objects.get(id=category_id)

        if Item.objects.filter(item_name=item_name).exists():
            messages.warning(request, 'Item already exits.')
            return redirect('add_items')
        else:
            item = Item(
                item_pic=item_pic,
                item_name=item_name,
                specification=specification,
                quantity=quantity,
                total_amount=total_amount,
                category_id=category,
                date_of_purchase=date_of_purchase,
                department_id=department,
                location_id=location,
                purpose_id=purpose
            )
        item.save()
        messages.success(request, item.item_name + " " + "Successfully Added.")
        return redirect('add_items')

    context = {
        'category': category,
        'department': department,
        'location': location,
        'purpose': purpose
    }

    return render(request, 'Hod/add_items.html', context)


@login_required(login_url='/')
def VIEW_ITEMS(request):
    item = Item.objects.all()

    context = {
        'item': item,
    }
    return render(request, 'Hod/view_items.html', context)


@login_required(login_url='/')
def EDIT_ITEMS(request, id):
    item = Item.objects.filter(id=id)
    category = Category.objects.all()
    department = Department.objects.all()
    location = Location.objects.all()
    purpose = Purpose.objects.all()

    context = {
        'item': item,
        'category': category,
        'department': department,
        'location': location,
        'purpose': purpose
    }
    return render(request, 'Hod/edit_items.html', context)


@login_required(login_url='/')
def UPDATE_ITEMS(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item_pic = request.FILES.get('item_pic')
        item_name = request.POST.get('item_name')
        specification = request.POST.get('specification')
        quantity = request.POST.get('quantity')
        total_amount = request.POST.get('total_amount')
        category_id = request.POST.get('category_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        department_id = request.POST.get('department_id')
        location_id = request.POST.get('location_id')
        purpose_id = request.POST.get('purpose_id')

        item = Item.objects.get(id=item_id)

        if item_pic != None and item_pic != "":
            item.item_pic = item_pic

        item.item_name = item_name
        item.specification = specification
        item.quantity = quantity
        item.total_amount = total_amount
        category = Category.objects.get(id=category_id)
        item.category_id = category
        item.date_of_purchase = date_of_purchase
        department = Department.objects.get(id=department_id)
        item.department_id = department

        location = Location.objects.get(id=location_id)
        item.location_id = location

        purpose = Purpose.objects.get(id=purpose_id)
        item.purpose_id = purpose

        item.save()
        messages.success(request, 'Item Successfully Updated.')
        return redirect('view_items')

    return render(request, 'Hod/edit_items.html')


@login_required(login_url='/')
def DELETE_ITEMS(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    messages.success(request, 'Item Successfully Deleted.')
    return redirect('view_items')


@login_required(login_url='/')
def ADD_DEPARTMENTS(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')

        department = Department(
            name=department_name
        )
        department.save()
        messages.success(request, 'Department Successfully Added.')
        return redirect('add_departments')

    return render(request, 'Hod/add_department.html')


@login_required(login_url='/')
def VIEW_DEPARTMENTS(request):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    return render(request, 'Hod/view_departments.html', context)


@login_required(login_url='/')
def EDIT_DEPARTMENTS(request, id):
    department = Department.objects.get(id=id)

    context = {
        'department': department,
    }
    return render(request, 'Hod/edit_departments.html', context)


@login_required(login_url='/')
def UPDATE_DEPARTMENTS(request):
    if request.method == "POST":
        department_name = request.POST.get('name')
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id=department_id)
        department.name = department_name
        department.save()
        messages.success(request, 'Department Successfully Updated')
        return redirect('view_departments')

    return render(request, 'Hod/edit_departments.html')


@login_required(login_url='/')
def DELETE_DEPARTMENTS(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.success(request, 'Department Successfully Deleted.')
    return redirect('view_departments')


@login_required(login_url='/')
def ADD_LOCATIONS(request):
    if request.method == "POST":
        location_name = request.POST.get('location_name')

        location = Location(
            name=location_name
        )
        location.save()
        messages.success(request, 'Location Successfully Added.')
        return redirect('add_locations')

    return render(request, 'Hod/add_locations.html')


@login_required(login_url='/')
def VIEW_LOCATIONS(request):
    location = Location.objects.all()
    context = {
        'location': location,
    }
    return render(request, 'Hod/view_locations.html', context)


@login_required(login_url='/')
def EDIT_LOCATIONS(request, id):
    location = Location.objects.get(id=id)

    context = {
        'location': location,
    }
    return render(request, 'Hod/edit_locations.html', context)


@login_required(login_url='/')
def UPDATE_LOCATIONS(request):
    if request.method == "POST":
        location_name = request.POST.get('name')
        location_id = request.POST.get('location_id')

        location = Location.objects.get(id=location_id)
        location.name = location_name
        location.save()
        messages.success(request, 'Location Successfully Updated')
        return redirect('view_locations')

    return render(request, 'Hod/edit_locations.html')


@login_required(login_url='/')
def DELETE_LOCATIONS(request, id):
    location = Location.objects.get(id=id)
    location.delete()
    messages.success(request, 'Location Successfully Deleted.')
    return redirect('view_locations')


@login_required(login_url='/')
def ADD_PURPOSES(request):
    if request.method == "POST":
        purpose_name = request.POST.get('purpose_name')

        purpose = Purpose(
            name=purpose_name
        )
        purpose.save()
        messages.success(request, 'Purpose Successfully Added.')
        return redirect('add_purposes')

    return render(request, 'Hod/add_purposes.html')


@login_required(login_url='/')
def VIEW_PURPOSES(request):
    purpose = Purpose.objects.all()
    context = {
        'purpose': purpose,
    }
    return render(request, 'Hod/view_purposes.html', context)


@login_required(login_url='/')
def EDIT_PURPOSES(request, id):
    purpose = Purpose.objects.get(id=id)

    context = {
        'purpose': purpose,
    }
    return render(request, 'Hod/edit_purposes.html', context)


@login_required(login_url='/')
def UPDATE_PURPOSES(request):
    if request.method == "POST":
        purpose_name = request.POST.get('name')
        purpose_id = request.POST.get('purpose_id')

        purpose = Purpose.objects.get(id=purpose_id)
        purpose.name = purpose_name
        purpose.save()
        messages.success(request, 'Purpose Successfully Updated')
        return redirect('view_purposes')

    return render(request, 'Hod/edit_purposes.html')


@login_required(login_url='/')
def DELETE_PURPOSES(request, id):
    purpose = Purpose.objects.get(id=id)
    purpose.delete()
    messages.success(request, 'Purpose Successfully Deleted.')
    return redirect('view_purposes')


@login_required(login_url='/')
def ADD_CATEGORIES(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')

        category = Category(
            name=category_name
        )
        category.save()
        messages.success(request, 'Category Successfully Added.')
        return redirect('add_categories')

    return render(request, 'Hod/add_categories.html')


@login_required(login_url='/')
def VIEW_CATEGORIES(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'Hod/view_categories.html', context)


@login_required(login_url='/')
def EDIT_CATEGORIES(request, id):
    category = Category.objects.get(id=id)

    context = {
        'category': category,
    }
    return render(request, 'Hod/edit_categories.html', context)


@login_required(login_url='/')
def UPDATE_CATEGORIES(request):
    if request.method == "POST":
        category_name = request.POST.get('name')
        category_id = request.POST.get('category_id')

        category = Category.objects.get(id=category_id)
        category.name = category_name
        category.save()
        messages.success(request, 'Category Successfully Updated')
        return redirect('view_categories')

    return render(request, 'Hod/edit_categories.html')


@login_required(login_url='/')
def DELETE_CATEGORIES(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Category Successfully Deleted.')
    return redirect('view_categories')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken!')
            return redirect('add_cheeStaff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_cheeStaff')
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, email=email, username=username,
                              profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
            )
            staff.save()
            messages.success(request, 'Staff Successfully Added!')
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff,
    }

    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.filter(id=id)

    context = {
        'staff': staff
    }
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        user.save()

        messages.success(request, 'Staff Updated Successfully!')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Record Successfully Deleted!')
    return redirect('view_staff')


@login_required(login_url='/')
def LEAVE_VIEW(request):
    staff_leave = StaffLeave.objects.all()

    context = {
        'staff_leave': staff_leave,
    }
    return render(request, 'Hod/staff_leave.html', context)


@login_required(login_url='/')
def APPROVE_LEAVE(request, id):
    leave = StaffLeave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('leave_view')


@login_required(login_url='/')
def DISAPPROVE_LEAVE(request, id):
    leave = StaffLeave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('leave_view')


def FEEDBACK(request):
    feedback = StaffFeedback.objects.all()

    see_feedback = StaffFeedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback,
        'see_feedback': see_feedback,
    }
    return render(request, 'Hod/staff_feedback.html', context)


def FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = StaffFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()

    return redirect('feedback')


def ITEM_REQUEST(request):
    staff_request = ItemRequest.objects.all()

    context = {
        'staff_request': staff_request,
    }
    return render(request, 'Hod/staff_request.html', context)


def APPROVE_REQUEST(request, id):
    request = ItemRequest.objects.get(id=id)
    request.status = 1
    request.save()
    return redirect('request_view')


def DENY_REQUEST(request, id):
    request = ItemRequest.objects.get(id=id)
    request.status = 2
    request.save()
    return redirect('request_view')


def ADD_MEDICINES(request):
    location = Location.objects.all()

    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name')
        quantity = request.POST.get('quantity')
        manufacture = request.POST.get('manufacture')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        location_id = request.POST.get('location_id')

        location = Location.objects.get(id=location_id)

        if Medicine.objects.filter(medicine_name=medicine_name).exists():
            messages.warning(request, 'Medicine already exits.')
            return redirect('add_medicines')
        else:
            medicine = Medicine(
                medicine_name=medicine_name,
                quantity=quantity,
                manufacture=manufacture,
                valid_from=valid_from,
                valid_to=valid_to,
                location_id=location,
            )
        medicine.save()
        messages.success(request, medicine.medicine_name + " " + "Successfully Added.")
        return redirect('add_medicines')

    context = {
        'location': location,
    }

    return render(request, 'Hod/add_medicines.html', context)


 
def VIEW_MEDICINES(request):
    medicine = Medicine.objects.all().order_by("-created_at")
 
    context = {
        "medicine": medicine,
      
    }
    return render(request, 'Hod/view_medicines.html', context)
