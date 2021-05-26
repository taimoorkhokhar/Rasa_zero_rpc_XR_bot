from django.contrib import admin
from . import models

# Register all models here
admin.site.register(models.Collective)
admin.site.register(models.Channel)
admin.site.register(models.Assistant)
admin.site.register(models.Intent)
admin.site.register(models.Response)
admin.site.register(models.IntentExamples)

