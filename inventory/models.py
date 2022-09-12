from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now


# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        ('1', 'HOD'),
        ('2', 'CHEE'),
        ('3', 'DCEC')
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    item_pic = models.ImageField(upload_to='media/item_pic')
    item_name = models.CharField(max_length=100)
    specification = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    total_amount = models.FloatField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    date_of_purchase = models.DateField()
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    location_id = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    purpose_id = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username


class StaffLeave(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name


class StaffFeedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name


class ItemRequest(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    date_of_request = models.DateField()
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    purpose_id = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING)
    remarks = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField()))


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    receive_quantity = models.CharField(max_length=100)
    reorder_level = models.IntegerField(default='0', blank="True", null="True")
    manufacture = models.CharField(max_length=100, blank="True", null="True")
    valid_from = models.DateField()
    valid_to = models.DateField()
    location_id = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    objects = ExpiredManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicine_name

    @property
    def get_remaining_days(self):
        difference =  self.valid_to - self.valid_from
        return difference.days

