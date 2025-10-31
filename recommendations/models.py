from django.db import models


class Recommendation(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    image = models.ImageField(upload_to="movie/images/", default="movie/images/default.jpg")

    def __str__(self) -> str:
        return self.title
