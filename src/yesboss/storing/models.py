from os import path
from datetime import datetime
from django.db import models

def get_file_folder(instance, filename):
    today = datetime.now()
    return path.join("store", today.strftime("%Y"), today.strftime("%m"), filename)

class Files(models.Model):

    id = models.BigAutoField(primary_key=True)
    file_type = models.SmallIntegerField(blank=True, null=True)
    file_path = models.FileField(upload_to=get_file_folder, max_length=300, blank=False, null=False)

    created_dt = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, editable=False)
    updated_dt = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.file_type is None:
            self.file_type = 1

        super(Files, self).save(*args, **kwargs)
