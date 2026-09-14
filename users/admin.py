from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import EmployeeSetup, PublicUserProfile


#!- --- ADVANCED EMPLOYEE SETUP ADMIN CONFIGURATION ---
@admin.register(EmployeeSetup)
class EmployeeSetupAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN THE LIST VIEW
    list_display = (
        'EMPLOYEE_FULL_NAME',
        'EMPLOYEE_EMAIL',
        'role_badge',
        'EMPLOYEE_MOBILE_NO',
        'EMPLOYEE_IP',
        'EMPLOYEE_CREATED_AT',
    )
    
    #!- FILTER OPTIONS IN THE RIGHT SIDEBAR
    list_filter = (
        'EMPLOYEE_ROLE',
        'EMPLOYEE_CREATED_AT',
        'EMPLOYEE_UPDATED_AT',
    )
    
    #!- SEARCHABLE FIELDS IN THE ADMIN BAR
    search_fields = (
        'EMPLOYEE_FULL_NAME',
        'EMPLOYEE_EMAIL',
        'EMPLOYEE_MOBILE_NO',
        'EMPLOYEE_IP',
    )
    
    #!- DEFAULT SORTING ORDER
    ordering = ('-EMPLOYEE_CREATED_AT',)
    
    #!- READONLY AUDIT FIELDS
    readonly_fields = ('EMPLOYEE_CREATED_AT', 'EMPLOYEE_UPDATED_AT')
    
    #!- ITEMS PER PAGE
    list_per_page = 25
    
    #!- FIELDSETS LAYOUT FOR DETAILED EDITING
    fieldsets = (
        ('PERSONAL INFORMATION', {
            'fields': (
                'EMPLOYEE_FULL_NAME',
                'EMPLOYEE_EMAIL',
                'EMPLOYEE_MOBILE_NO',
                'EMPLOYEE_ADDRESS',
            )
        }),
        ('ROLE & SECURITY', {
            'fields': (
                'EMPLOYEE_ROLE',
                'EMPLOYEE_PASSWORD',
                'EMPLOYEE_IP',
            )
        }),
        ('AUDIT METADATA', {
            'fields': (
                'EMPLOYEE_CREATED_BY',
                'EMPLOYEE_MODIFIED_BY',
                'EMPLOYEE_CREATED_AT',
                'EMPLOYEE_UPDATED_AT',
            ),
            'classes': ('collapse',),
        }),
    )

    #!- CUSTOM ROLE BADGE DISPLAY METHOD
    @admin.display(description='ROLE')
    def role_badge(self, obj):
        #!- STYLED BADGE FOR EMPLOYEE ROLE
        if not obj or not getattr(obj, 'EMPLOYEE_ROLE', None):
            return '-'
        color_map = {
            'ADMIN': '#c2410c',
            'MANAGER': '#1f6f5c',
            'CASHIER': '#2563eb',
            'DELIVERY_MAN': '#d97706',
            'STAFF': '#4b5563',
        }
        color = color_map.get(obj.EMPLOYEE_ROLE, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 4px 10px; font-weight: 600; font-size: 11px; letter-spacing: 0.5px;">{}</span>',
            color,
            obj.get_EMPLOYEE_ROLE_display()
        )


#!- --- ADVANCED PUBLIC USER PROFILE ADMIN CONFIGURATION ---
@admin.register(PublicUserProfile)
class PublicUserProfileAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN THE LIST VIEW
    list_display = (
        'PUBLIC_USER_FULL_NAME',
        'PUBLIC_USER_EMAIL',
        'PUBLIC_USER_MOBILE_NO',
        'PUBLIC_USER_IP',
        'profile_image_preview',
        'PUBLIC_USER_CREATED_AT',
    )
    
    #!- FILTER OPTIONS IN THE RIGHT SIDEBAR
    list_filter = (
        'PUBLIC_USER_CREATED_AT',
        'PUBLIC_USER_UPDATED_AT',
    )
    
    #!- SEARCHABLE FIELDS
    search_fields = (
        'PUBLIC_USER_FULL_NAME',
        'PUBLIC_USER_EMAIL',
        'PUBLIC_USER_MOBILE_NO',
        'PUBLIC_USER_IP',
    )
    
    #!- DEFAULT SORTING ORDER
    ordering = ('-PUBLIC_USER_CREATED_AT',)
    
    #!- READONLY AUDIT AND PREVIEW FIELDS
    readonly_fields = ('PUBLIC_USER_CREATED_AT', 'PUBLIC_USER_UPDATED_AT', 'profile_image_preview')
    
    #!- ITEMS PER PAGE
    list_per_page = 25
    
    #!- FIELDSETS LAYOUT FOR DETAILED EDITING
    fieldsets = (
        ('PUBLIC USER PROFILE INFO', {
            'fields': (
                'PUBLIC_USER_FULL_NAME',
                'PUBLIC_USER_EMAIL',
                'PUBLIC_USER_MOBILE_NO',
                'PUBLIC_USER_ADDRESS',
                'PUBLIC_USER_PROFILE_IMAGE',
                'profile_image_preview',
            )
        }),
        ('SECURITY & TRACKING', {
            'fields': (
                'PUBLIC_USER_PASSWORD',
                'PUBLIC_USER_IP',
            )
        }),
        ('AUDIT METADATA', {
            'fields': (
                'PUBLIC_USER_CREATED_BY',
                'PUBLIC_USER_MODIFIED_BY',
                'PUBLIC_USER_CREATED_AT',
                'PUBLIC_USER_UPDATED_AT',
            ),
            'classes': ('collapse',),
        }),
    )

    #!- CUSTOM PROFILE IMAGE PREVIEW METHOD
    @admin.display(description='PROFILE PREVIEW')
    def profile_image_preview(self, obj):
        #!- INLINE PREVIEW OF PUBLIC USER PROFILE IMAGE
        if obj and getattr(obj, 'PUBLIC_USER_PROFILE_IMAGE', None) and obj.PUBLIC_USER_PROFILE_IMAGE:
            return format_html(
                '<img src="{}" style="width: 42px; height: 42px; object-fit: cover; border: 1px solid #e4e7eb;" />',
                obj.PUBLIC_USER_PROFILE_IMAGE.url
            )
        return mark_safe('<span style="color: #9ca3af;">NO IMAGE</span>')
