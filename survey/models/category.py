# -*- coding: utf-8 -*-

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .survey import Survey


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=400)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("Survey"), related_name="categories")
    order = models.IntegerField(_("Display order"), blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2000, blank=True, null=True)
    wasp_index = models.IntegerField(_("Wasp index"), blank=True, null=True, default=0)
    
    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        if self.wasp_index>0:
            return self.name+" (wasp: "+str(self.wasp_index)+")"
        else:
            return self.name

    def slugify(self):
        return slugify(str(self))
