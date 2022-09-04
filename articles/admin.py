from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    
    def clean(self):
        main_tag_count = 0
        for form in self.forms:
            if form.cleaned_data['is_main']:
                main_tag_count += 1
            if main_tag_count > 1:
                raise ValidationError('Основным может быть только один раздел')
            elif main_tag_count == 0:
                raise ValidationError('Укажите основной раздел')
        return super().clean()
        

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at', ]
    inlines = [ScopeInline, ]
    list_filter = ['published_at', ]
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
