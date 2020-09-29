# -*- coding: utf-8 -*-

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .survey import Survey


class Category(models.Model):

    DEFAULT="default"
    IMAGE_SELECT_MULTIPLE="image select multiple"
    IMAGE_FEEL="image feel"

    TEMPLATE_TYPES = (
        (DEFAULT, _("Default")),
        (IMAGE_SELECT_MULTIPLE, _("Image select multiple")),
        (IMAGE_FEEL, _("Image feel"))
    )

    name = models.CharField(_("Name"), max_length=400)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("Survey"), related_name="categories")
    order = models.IntegerField(_("Display order"), blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2000, blank=True, null=True)
    template = models.CharField(_("Template"), max_length=200, choices=TEMPLATE_TYPES, default=DEFAULT)

    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))
