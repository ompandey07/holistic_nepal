from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Gallery,
    GalleryImage,
    News,
    NewsImage,
    UnitSetup,
    ProductCategory,
    ProductSetup,
    ProductImage,
    ProductRating,
    ProductOrder,
    HospitalInfo,
    HospitalService,
    HospitalServiceTag,
    Service,
)


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


#!- --- GALLERY ADMIN CONFIGURATION ---
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'GALLERY_TITLE',
        'image_thumbnail',
        'GALLERY_CREATED_BY',
        'GALLERY_CREATED_AT',
    )
    
    #!- FILTER OPTIONS IN RIGHT SIDEBAR
    list_filter = ('GALLERY_CREATED_AT', 'GALLERY_MODIFIED_AT')
    
    #!- SEARCHABLE FIELDS
    search_fields = ('GALLERY_TITLE', 'GALLERY_DESCRIPTION')
    
    #!- SORTING ORDER
    ordering = ('-GALLERY_CREATED_AT',)
    
    #!- READONLY FIELDS
    readonly_fields = ('GALLERY_CREATED_AT', 'GALLERY_MODIFIED_AT', 'image_thumbnail')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    #!- CUSTOM IMAGE THUMBNAIL RENDERER
    @admin.display(description='THUMBNAIL')
    def image_thumbnail(self, obj):
        #!- RENDER GALLERY IMAGE THUMBNAIL
        if obj and getattr(obj, 'GALLERY_IMAGE', None) and obj.GALLERY_IMAGE:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border: 1px solid #e4e7eb;" />',
                obj.GALLERY_IMAGE.url
            )
        return mark_safe('<span style="color: #9ca3af;">NO IMAGE</span>')


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


#!- --- NEWS ADMIN CONFIGURATION ---
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'NEWS_TITLE',
        'news_type_badge',
        'news_image_preview',
        'NEWS_CREATED_BY',
        'NEWS_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('NEWS_TYPE', 'NEWS_CREATED_AT', 'NEWS_MODIFIED_AT')
    
    #!- SEARCHABLE FIELDS
    search_fields = ('NEWS_TITLE', 'NEWS_DESCRIPTION')
    
    #!- SORTING ORDER
    ordering = ('-NEWS_CREATED_AT',)
    
    #!- READONLY FIELDS
    readonly_fields = ('NEWS_CREATED_AT', 'NEWS_MODIFIED_AT', 'news_image_preview')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    #!- CUSTOM NEWS TYPE BADGE
    @admin.display(description='TYPE')
    def news_type_badge(self, obj):
        #!- STYLED BADGE FOR NEWS TYPE
        if not obj or not getattr(obj, 'NEWS_TYPE', None):
            return '-'
        color_map = {
            'GENERAL': '#4b5563',
            'ANNOUNCEMENT': '#c2410c',
            'EVENT': '#2563eb',
            'UPDATE': '#1f6f5c',
            'NOTICE': '#d97706',
            'BLOG': '#8b5cf6',
            'PRESS_RELEASE': '#ec4899',
        }
        color = color_map.get(obj.NEWS_TYPE, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 4px 9px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            obj.get_NEWS_TYPE_display()
        )

    #!- CUSTOM NEWS IMAGE PREVIEW
    @admin.display(description='PREVIEW')
    def news_image_preview(self, obj):
        #!- RENDER NEWS IMAGE PREVIEW
        if obj and getattr(obj, 'NEWS_IMAGE', None) and obj.NEWS_IMAGE:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border: 1px solid #e4e7eb;" />',
                obj.NEWS_IMAGE.url
            )
        return mark_safe('<span style="color: #9ca3af;">NO IMAGE</span>')


#!- --- UNIT SETUP ADMIN CONFIGURATION ---
@admin.register(UnitSetup)
class UnitSetupAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'UNIT_NAME',
        'UNIT_SYMBOL',
        'UNIT_CREATED_BY',
        'UNIT_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('UNIT_CREATED_AT',)
    
    #!- SEARCHABLE FIELDS
    search_fields = ('UNIT_NAME', 'UNIT_SYMBOL')
    
    #!- SORTING ORDER
    ordering = ('UNIT_NAME',)
    
    #!- READONLY FIELDS
    readonly_fields = ('UNIT_CREATED_AT', 'UNIT_MODIFIED_AT')
    
    #!- ITEMS PER PAGE
    list_per_page = 25


#!- --- PRODUCT CATEGORY ADMIN CONFIGURATION ---
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'CATEGORY_NAME',
        'CATEGORY_TAG',
        'category_image_preview',
        'CATEGORY_CREATED_BY',
        'CATEGORY_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('CATEGORY_CREATED_AT',)
    
    #!- SEARCHABLE FIELDS
    search_fields = ('CATEGORY_NAME', 'CATEGORY_TAG')
    
    #!- SORTING ORDER
    ordering = ('CATEGORY_NAME',)
    
    #!- READONLY FIELDS
    readonly_fields = ('CATEGORY_CREATED_AT', 'CATEGORY_MODIFIED_AT', 'category_image_preview')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    #!- CUSTOM CATEGORY IMAGE PREVIEW
    @admin.display(description='IMAGE')
    def category_image_preview(self, obj):
        if obj and getattr(obj, 'CATEGORY_IMAGE', None) and obj.CATEGORY_IMAGE:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.CATEGORY_IMAGE.url
            )
        return format_html('<span style="color: #999; font-style: italic;">No Image</span>')



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

#!- --- PRODUCT SETUP ADMIN CONFIGURATION ---
@admin.register(ProductSetup)
class ProductSetupAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'PRODUCT_NAME',
        'PRODUCT_CATEGORY',
        'PRODUCT_PRICE',
        'PRODUCT_UNIT',
        'product_image_preview',
        'PRODUCT_CREATED_BY',
        'PRODUCT_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('PRODUCT_CATEGORY', 'PRODUCT_UNIT', 'PRODUCT_CREATED_AT')
    
    #!- SEARCHABLE FIELDS
    search_fields = ('PRODUCT_NAME', 'PRODUCT_SLUG', 'PRODUCT_DESCRIPTION')

    #!- PREPOPULATED FIELDS
    prepopulated_fields = {'PRODUCT_SLUG': ('PRODUCT_NAME',)}
    
    #!- SORTING ORDER
    ordering = ('-PRODUCT_CREATED_AT',)
    
    #!- READONLY FIELDS
    readonly_fields = ('PRODUCT_CREATED_AT', 'PRODUCT_MODIFIED_AT', 'product_image_preview')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    #!- CUSTOM PRODUCT IMAGE PREVIEW
    @admin.display(description='IMAGE')
    def product_image_preview(self, obj):
        #!- RENDER PRODUCT IMAGE THUMBNAIL
        if obj and getattr(obj, 'PRODUCT_IMAGE', None) and obj.PRODUCT_IMAGE:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border: 1px solid #e4e7eb;" />',
                obj.PRODUCT_IMAGE.url
            )
        return mark_safe('<span style="color: #9ca3af;">NO IMAGE</span>')


#!- --- PRODUCT RATING ADMIN CONFIGURATION ---
@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'PRODUCT_RATING_PRODUCT',
        'reviewer_name',
        'reviewer_location',
        'rating_stars_display',
        'IS_FEATURED',
        'IS_VERIFIED',
        'PRODUCT_RATING_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('IS_FEATURED', 'IS_VERIFIED', 'PRODUCT_RATING_VALUE', 'PRODUCT_RATING_CREATED_AT')
    
    #!- SEARCHABLE FIELDS
    search_fields = (
        'PRODUCT_RATING_PRODUCT__PRODUCT_NAME',
        'REVIEWER_NAME',
        'REVIEWER_LOCATION',
        'PRODUCT_RATING_USER__PUBLIC_USER_FULL_NAME',
        'COMMENT_ENG',
        'COMMENT_NEP',
        'PRODUCT_RATING_COMMENT',
    )
    
    #!- FIELDSETS FOR ORGANIZED FORM
    fieldsets = (
        ('Target Product & Rating', {
            'fields': ('PRODUCT_RATING_PRODUCT', 'PRODUCT_RATING_VALUE', 'IS_FEATURED', 'IS_VERIFIED')
        }),
        ('Reviewer Info', {
            'fields': ('REVIEWER_NAME', 'REVIEWER_LOCATION', 'PRODUCT_RATING_USER')
        }),
        ('Review Comments', {
            'fields': ('COMMENT_ENG', 'COMMENT_NEP', 'PRODUCT_RATING_COMMENT')
        }),
        ('Timestamps', {
            'fields': ('PRODUCT_RATING_CREATED_AT', 'PRODUCT_RATING_MODIFIED_AT'),
            'classes': ('collapse',),
        }),
    )
    
    #!- SORTING ORDER
    ordering = ('-IS_FEATURED', '-PRODUCT_RATING_CREATED_AT')
    
    #!- READONLY FIELDS
    readonly_fields = ('PRODUCT_RATING_CREATED_AT', 'PRODUCT_RATING_MODIFIED_AT')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    #!- CUSTOM STYLING FOR RATING DISPLAY
    @admin.display(description='RATING STARS')
    def rating_stars_display(self, obj):
        #!- RENDER VISUAL STAR RATING
        if not obj or obj.PRODUCT_RATING_VALUE is None:
            return '-'
        val = float(obj.PRODUCT_RATING_VALUE)
        full_stars = '★' * int(val)
        return format_html(
            '<span style="color: #f59e0b; font-size: 14px; font-weight: 600;">{} ({})</span>',
            full_stars,
            val
        )


#!- --- PRODUCT ORDER ADMIN CONFIGURATION ---
@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    #!- DISPLAY FIELDS IN LIST VIEW
    list_display = (
        'PRODUCT_ORDER_ID',
        'customer_display',
        'product_display_name',
        'items_count_or_qty',
        'order_amount_formatted',
        'status_badge',
        'ORDER_SOURCE',
        'PRODUCT_ORDER_CREATED_AT',
    )
    
    #!- FILTER OPTIONS
    list_filter = ('PRODUCT_ORDER_STATUS', 'ORDER_SOURCE', 'PAYMENT_METHOD', 'IS_PAID', 'PRODUCT_ORDER_CREATED_AT')
    
    #!- SEARCHABLE FIELDS
    search_fields = (
        'PRODUCT_ORDER_ID',
        'SHIPPING_NAME',
        'SHIPPING_PHONE',
        'SHIPPING_EMAIL',
        'CUSTOMER__PUBLIC_USER_FULL_NAME',
        'PRODUCT_ORDER_USER__EMPLOYEE_FULL_NAME',
        'PRODUCT_ORDER_PRODUCT__PRODUCT_NAME',
    )
    
    #!- SORTING ORDER
    ordering = ('-PRODUCT_ORDER_CREATED_AT',)
    
    #!- READONLY FIELDS
    readonly_fields = ('PRODUCT_ORDER_ID', 'PRODUCT_ORDER_CREATED_AT', 'PRODUCT_ORDER_MODIFIED_AT')
    
    #!- ITEMS PER PAGE
    list_per_page = 25

    @admin.display(description='CUSTOMER / USER')
    def customer_display(self, obj):
        if obj.CUSTOMER:
            return f"Client: {obj.CUSTOMER.PUBLIC_USER_FULL_NAME}"
        elif obj.PRODUCT_ORDER_USER:
            return f"Staff: {obj.PRODUCT_ORDER_USER.EMPLOYEE_FULL_NAME}"
        return obj.SHIPPING_NAME or "Guest / Unassigned"

    @admin.display(description='AMOUNT')
    def order_amount_formatted(self, obj):
        amt = obj.order_amount
        return f"Rs {amt:,.2f}"

    #!- CUSTOM ORDER STATUS BADGE
    @admin.display(description='STATUS')
    def status_badge(self, obj):
        #!- STYLED BADGE FOR ORDER STATUS
        if not obj or not getattr(obj, 'PRODUCT_ORDER_STATUS', None):
            return '-'
        color_map = {
            'PENDING': '#c2410c',
            'CONFIRMED': '#2563eb',
            'PROCESSING': '#d97706',
            'SHIPPED': '#8b5cf6',
            'DELIVERED': '#1f6f5c',
            'CANCELLED': '#dc2626',
        }
        color = color_map.get(obj.PRODUCT_ORDER_STATUS, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 4px 10px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            obj.get_PRODUCT_ORDER_STATUS_display()
        )


#!- --- HOSPITAL INFO ADMIN CONFIGURATION ---
@admin.register(HospitalInfo)
class HospitalInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'HERO_TITLE_ENG', 'HERO_TITLE_NEP', 'CONTACT_PHONE', 'IS_ACTIVE', 'UPDATED_AT')
    fieldsets = (
        ('General & Hero Banner', {
            'fields': (
                'IS_ACTIVE',
                'HERO_BANNER_IMAGE',
                ('HERO_TITLE_ENG', 'HERO_TITLE_NEP'),
                ('HERO_SUBTITLE_ENG', 'HERO_SUBTITLE_NEP'),
            )
        }),
        ('Introduction Section', {
            'fields': (
                ('INTRO_TITLE_ENG', 'INTRO_TITLE_NEP'),
                'INTRO_TEXT_NEP',
                'INTRO_TEXT_ENG',
            )
        }),
        ('Conditions & Diseases Treated', {
            'fields': (
                ('DISEASES_TITLE_ENG', 'DISEASES_TITLE_NEP'),
                'DISEASES_TEXT_NEP',
                'DISEASES_TEXT_ENG',
            )
        }),
        ('Paralysis Treatment Feature', {
            'fields': (
                ('PARALYSIS_TITLE_ENG', 'PARALYSIS_TITLE_NEP'),
                'PARALYSIS_BANNER_IMAGE',
                'PARALYSIS_DESC_NEP',
                'PARALYSIS_DESC_ENG',
            )
        }),
        ('Contact Information', {
            'fields': (
                'CONTACT_PHONE',
                'CONTACT_EMAIL',
                ('CONTACT_LOCATION_ENG', 'CONTACT_LOCATION_NEP'),
            )
        }),
    )


#!- --- HOSPITAL SERVICE ADMIN CONFIGURATION ---
@admin.register(HospitalService)
class HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ('SERVICE_ORDER', 'SERVICE_NAME_NEP', 'SERVICE_NAME_ENG', 'image_thumbnail', 'IS_ACTIVE')
    list_display_links = ('SERVICE_NAME_NEP',)
    list_editable = ('SERVICE_ORDER', 'IS_ACTIVE')
    list_filter = ('IS_ACTIVE',)
    search_fields = ('SERVICE_NAME_NEP', 'SERVICE_NAME_ENG')
    ordering = ('SERVICE_ORDER', 'id')

    @admin.display(description='IMAGE')
    def image_thumbnail(self, obj):
        if obj and obj.SERVICE_IMAGE:
            return format_html(
                '<img src="{}" style="width: 60px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid #e4e7eb;" />',
                obj.SERVICE_IMAGE.url
            )
        return mark_safe('<span style="color: #9ca3af;">NO IMAGE</span>')


#!- --- HOSPITAL SERVICE TAG ADMIN CONFIGURATION ---
@admin.register(HospitalServiceTag)
class HospitalServiceTagAdmin(admin.ModelAdmin):
    list_display = ('TAG_ORDER', 'TAG_LABEL_NEP', 'TAG_LABEL_ENG', 'IS_ACTIVE')
    list_display_links = ('TAG_LABEL_NEP',)
    list_editable = ('TAG_ORDER', 'IS_ACTIVE')
    list_filter = ('IS_ACTIVE',)
    search_fields = ('TAG_LABEL_NEP', 'TAG_LABEL_ENG')
    ordering = ('TAG_ORDER', 'id')


#!- --- CLINICAL SERVICE ADMIN CONFIGURATION ---
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug', 'order')
    list_display_links = ('name_en',)
    list_editable = ('order',)
    search_fields = ('name_en', 'name_np', 'slug')
    ordering = ('order', 'id')
    filter_horizontal = ('related_services',)

