from django.db import models

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ideas/', blank=True, null=True)

    expected_devtool = models.CharField(max_length=100, blank=True)
    interest = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE)
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.idea.title} - {self.is_starred}'
    
class DevTool(models.Model):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name