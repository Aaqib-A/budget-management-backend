from django.contrib import admin
from category.models import Category

# Register your models here.
# class DocumentInline(admin.TabularInline):  # TabularInline makes it look like a table
#     model = Document
#     extra = 1 
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields] #if field.name != 'client_id']
    search_fields = ["user__username", "category_name"]
    # inlines = [DocumentInline]
