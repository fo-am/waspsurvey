from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .question import Question

class Insect(models.Model):
    name = models.TextField(_("ID name"), blank=True, null=True)
    photo = models.ImageField(upload_to='static/image_uploads')
    location = models.TextField(_("Location"), blank=True, null=True)
    
