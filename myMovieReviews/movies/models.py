from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    running_time = models.IntegerField()
    content = models.TextField()
    release_year = models.IntegerField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def running_time_display(self):
        hours = self.running_time // 60
        minutes = self.running_time % 60

        if hours and minutes:
            return f"{hours}시간 {minutes}분"
        elif hours:
            return f"{hours}시간"
        else:
            return f"{minutes}분"

    def __str__(self):
        return self.title