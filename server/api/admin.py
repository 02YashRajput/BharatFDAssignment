from django.contrib import admin
from .models import Language, FAQ, Translation
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register the Language model in the admin
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code',)  # Display only the language code
    search_fields = ('code',)  # Make code searchable in the admin


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')  # Display question and creation date
    search_fields = ('question',)  # Make question searchable in the admin
    list_filter = ('created_at',)  # Filter by creation date

# Register the Translation model in the admin
@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    # Display FAQ question and language code
    list_display = ('faq_question', 'language_code', 'created_at')  

    # Make related fields searchable
    search_fields = ('faq__question', 'language__code')  # Searchable fields (use related model fields)
    
    # Filter by language
    list_filter = ('language',)

    # Custom method to show FAQ question in the admin list display
    def faq_question(self, obj):
        return obj.faq.question
    faq_question.admin_order_field = 'faq__question'  # Allow sorting by FAQ question
    faq_question.short_description = 'FAQ Question'  # Display name for the column

    # Custom method to show language code in the admin list display
    def language_code(self, obj):
        return obj.language.code
    language_code.admin_order_field = 'language__code'  # Allow sorting by language code
    language_code.short_description = 'Language'  # Display name for the column
