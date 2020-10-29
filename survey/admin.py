# -*- coding: utf-8 -*-

from django.contrib import admin

from survey.actions import make_published
from survey.exporter.csv import Survey2Csv
from survey.exporter.tex import Survey2Tex
from survey.models import Answer, Category, Question, Response, Survey, Image, Insect
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from copy import deepcopy

def model_copy(obj):
    obj = deepcopy(obj)
    obj.pk = None
    obj.save()

def duplicate_survey(modeladmin, request, queryset):
    for orig_survey in queryset:
        survey = deepcopy(orig_survey)
        survey.name = survey.name + ' -- Copy'
        survey.pk = None
        survey.save()
        catmap = {}
        for orig_cat in orig_survey.categories.all():
            cat = deepcopy(orig_cat)
            cat.survey = survey
            cat.pk = None
            cat.save()
            # need to map the categories so we can reconnect the qs to the new ones
            catmap[orig_cat.pk]=cat
        for orig_que in orig_survey.questions.all():
            que = deepcopy(orig_que)
            que.survey = survey
            que.category = catmap[orig_que.category.pk]
            que.pk = None
            que.save()
            
duplicate_survey.short_description = _("Duplicate")

class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ("order", "category")
    extra = 1
    formfield_overrides = {        
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':20})},
    }
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # limit the categories shown to the ones owned by this survey
        if db_field.name == "category":
            parent_id = request.resolver_match.kwargs["object_id"]
            kwargs["queryset"] = Category.objects.filter(survey=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    ordering = ("order",)
    

class SurveyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "need_logged_user", "template")
    list_filter = ("is_published", "need_logged_user")
    inlines = [CategoryInline, QuestionInline]
    actions = [make_published, Survey2Csv.export_as_csv, Survey2Tex.export_as_tex, duplicate_survey]


class AnswerBaseInline(admin.StackedInline):
    fields = ("question", "body")
    readonly_fields = ("question",)
    extra = 0
    model = Answer


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("interview_uuid", "survey", "created", "user")
    list_filter = ("survey", "created")
    date_hierarchy = "created"
    inlines = [AnswerBaseInline]
    # specifies the order as well as which fields to act on
    readonly_fields = ("survey", "created", "updated", "interview_uuid", "user")

class ImageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="/{}" />'.format(obj.photo))

    image_tag.short_description = 'Image'
    list_display = ['image_tag',]

class InsectAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="/{}" />'.format(obj.photo))

    image_tag.short_description = 'Insect'
    list_display = ['image_tag',]

#admin.site.register(Question, QuestionInline)
admin.site.register(Category)
admin.site.register(Insect, InsectAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
