from django.db import models

class Tour(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    duration = models.CharField(max_length=20)
    departure_location = models.CharField(max_length=100)
    transportation = models.CharField(max_length=50)
    start_dates = models.CharField(max_length=255)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.title