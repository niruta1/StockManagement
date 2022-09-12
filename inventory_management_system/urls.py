"""inventory_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views, Hod_Views, Staff_Views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.BASE, name='base'),

                  # LoginPath
                  path('', views.LOGIN, name='login'),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('doLogout', views.doLogout, name='logout'),

                  # Profile Update
                  path('Profile', views.PROFILE, name='Profile'),
                  path('Profile/update', views.PROFILE_UPDATE, name='Profile_update'),

                  # This is Hod Panel url
                  path('Home', Hod_Views.HOME, name='hod_home'),
                  path('Home/Items/Add', Hod_Views.ADD_ITEMS, name='add_items'),
                  path('Home/Items/Views', Hod_Views.VIEW_ITEMS, name='view_items'),
                  path('Home/Items/Edit/<str:id>', Hod_Views.EDIT_ITEMS, name='edit_items'),
                  path('Home/Items/Update', Hod_Views.UPDATE_ITEMS, name='update_items'),
                  path('Home/Items/Delete/<str:id>', Hod_Views.DELETE_ITEMS, name='delete_items'),

                  path('Home/Department/Add', Hod_Views.ADD_DEPARTMENTS, name='add_departments'),
                  path('Home/Department/View', Hod_Views.VIEW_DEPARTMENTS, name='view_departments'),
                  path('Home/Department/Edit/<str:id>', Hod_Views.EDIT_DEPARTMENTS, name='edit_departments'),
                  path('Home/Department/Update', Hod_Views.UPDATE_DEPARTMENTS, name='update_departments'),
                  path('Home/Department/Delete/<str:id>', Hod_Views.DELETE_DEPARTMENTS, name='delete_departments'),

                  path('Home/Location/Add', Hod_Views.ADD_LOCATIONS, name='add_locations'),
                  path('Home/Location/View', Hod_Views.VIEW_LOCATIONS, name='view_locations'),
                  path('Home/Location/Edit/<str:id>', Hod_Views.EDIT_LOCATIONS, name='edit_locations'),
                  path('Home/Location/Update', Hod_Views.UPDATE_LOCATIONS, name='update_locations'),
                  path('Home/Location/Delete/<str:id>', Hod_Views.DELETE_LOCATIONS, name='delete_locations'),

                  path('Home/Purpose/Add', Hod_Views.ADD_PURPOSES, name='add_purposes'),
                  path('Home/Purpose/View', Hod_Views.VIEW_PURPOSES, name='view_purposes'),
                  path('Home/Purpose/Edit/<str:id>', Hod_Views.EDIT_PURPOSES, name='edit_purposes'),
                  path('Home/Purpose/Update', Hod_Views.UPDATE_PURPOSES, name='update_purposes'),
                  path('Home/Purpose/Delete/<str:id>', Hod_Views.DELETE_PURPOSES, name='delete_purposes'),

                  path('Home/Category/Add', Hod_Views.ADD_CATEGORIES, name='add_categories'),
                  path('Home/Category/View', Hod_Views.VIEW_CATEGORIES, name='view_categories'),
                  path('Home/Category/Edit/<str:id>', Hod_Views.EDIT_CATEGORIES, name='edit_categories'),
                  path('Home/Category/Update', Hod_Views.UPDATE_CATEGORIES, name='update_categories'),
                  path('Home/Category/Delete/<str:id>', Hod_Views.DELETE_CATEGORIES, name='delete_categories'),

                  path('Home/Staff/Add', Hod_Views.ADD_STAFF, name='add_staff'),
                  path('Home/Staff/View', Hod_Views.VIEW_STAFF, name='view_staff'),
                  path('Home/Staff/Edit/<str:id>', Hod_Views.EDIT_STAFF, name='edit_staff'),
                  path('Home/Staff/Update', Hod_Views.UPDATE_STAFF, name='update_staff'),
                  path('Home/Staff/Delete/<str:admin>', Hod_Views.DELETE_STAFF, name='delete_staff'),

                  path('Home/Staff/LeaveView', Hod_Views.LEAVE_VIEW, name='leave_view'),
                  path('Home/Staff/ApproveLeave/<str:id>', Hod_Views.APPROVE_LEAVE, name='approve_leave'),
                  path('Home/Staff/DisapproveLeave/<str:id>', Hod_Views.DISAPPROVE_LEAVE, name='disapprove_leave'),

                  path('Home/Staff/Feedback', Hod_Views.FEEDBACK, name='feedback'),
                  path('Home/Staff/Feedback/Save', Hod_Views.FEEDBACK_SAVE, name='feedback_reply_save'),

                  path('Home/Staff/RequestView', Hod_Views.ITEM_REQUEST, name='request_view'),
                  path('Home/Staff/ApproveRequest/<str:id>', Hod_Views.APPROVE_REQUEST, name='approve_request'),
                  path('Home/Staff/DisapproveRequest/<str:id>', Hod_Views.DENY_REQUEST, name='deny_request'),

                  path('Home/Medicine/Add', Hod_Views.ADD_MEDICINES, name='add_medicines'),
                  path('Home/Medicine/View', Hod_Views.VIEW_MEDICINES, name='view_medicines'),

                  # This is Staff urls
                  path('Staff/Home', Staff_Views.HOME, name='staff_home'),
                  path('Staff/ApplyLeave', Staff_Views.APPLY_LEAVE, name='apply_leave'),
                  path('Staff/ApplyLeaveSave', Staff_Views.APPLY_LEAVE_SAVE, name='apply_leave_save'),

                  path('Staff/Feedback', Staff_Views.STAFF_FEEDBACK, name='staff_feedback'),
                  path('Staff/Feedback/Save', Staff_Views.STAFF_FEEDBACK_SAVE, name='feedback_save'),

                  path('Staff/ItemRequest', Staff_Views.ITEM_REQUEST, name='item_request'),
                  path('Staff/ItemRequestSave', Staff_Views.ITEM_REQUEST_SAVE, name='item_request_save'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
