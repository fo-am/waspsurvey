from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .question import Question

class Insect(models.Model):
    name = models.CharField(_("ID name"), max_length=200 )
    photo = models.ImageField(upload_to='static/image_uploads')
    location = models.CharField(_("Location"), blank=True, null=True, max_length=200 )
    
    def __str__(self):
        return str(self.name)
