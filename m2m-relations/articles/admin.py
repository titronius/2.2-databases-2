from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_of_main = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count_of_main += 1
        if count_of_main > 1:
            raise ValidationError('Основной раздел должен быть один!')
        elif count_of_main == 0:
            raise ValidationError('Не задан основной раздел!')
        return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
