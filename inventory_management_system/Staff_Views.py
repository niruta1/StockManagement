from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Staff, StaffLeave, StaffFeedback, Department, Purpose, ItemRequest
from django.contrib import messages


@login_required(login_url='/')
def HOME(request):
    return render(request, 'Staff/home.html')


@login_required(login_url='/')
def APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = StaffLeave.objects.filter(staff_id=staff_id)

        context = {
            'staff_leave_history': staff_leave_history,
        }
    return render(request, 'Staff/apply_leave.html', context)


@login_required(login_url='/')
def APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_date_to = request.POST.get('leave_date_to')
        category = request.POST.get('category')
        leave_reason = request.POST.get('leave_reason')

        staff = Staff.objects.get(admin=request.user.id)

        leave = StaffLeave(
            staff_id=staff,
            from_date=leave_date,
            to_date=leave_date_to,
            category=category,
            message=leave_reason,
        )
        leave.save()
        messages.success(request, 'Leave Successfully Sent')
    return redirect('apply_leave')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    feedback_history = StaffFeedback.objects.filter(staff_id=staff_id)

    context = {
        'feedback_history': feedback_history,
    }

    return render(request, 'Staff/feedback.html', context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin=request.user.id)
        feedback = StaffFeedback(
            staff_id=staff,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()
        messages.success(request, 'Feedback  Successfully Sent')
    return redirect('staff_feedback')


def ITEM_REQUEST(request):
    department = Department.objects.all()
    purpose = Purpose.objects.all()

    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id

        item_request_history = ItemRequest.objects.filter(staff_id=staff_id)

    context = {
        'department': department,
        'purpose': purpose,
        'item_request_history': item_request_history
    }

    return render(request, 'Staff/item_request.html', context)


def ITEM_REQUEST_SAVE(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')
        date_of_request = request.POST.get('date_of_request')
        department_id = request.POST.get('department_id')
        purpose_id = request.POST.get('purpose_id')
        remarks = request.POST.get('remarks')

        department = Department.objects.get(id=department_id)
        purpose = Purpose.objects.get(id=purpose_id)

        staff = Staff.objects.get(admin=request.user.id)

        itemRequest = ItemRequest(
            staff_id=staff,
            item_name=item_name,
            quantity=quantity,
            date_of_request=date_of_request,
            department_id=department,
            purpose_id=purpose,
            remarks=remarks

        )
        itemRequest.save()
        messages.success(request, itemRequest.item_name + " " + "Successfully Added.")
    return redirect('item_request')
