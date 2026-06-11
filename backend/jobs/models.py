from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    # We use JSONField to support multiselect values (stores lists like ['Draft', 'Requested'])
    status = models.JSONField(default=list, blank=True)
    category = models.JSONField(default=list, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='job_pics/', null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
