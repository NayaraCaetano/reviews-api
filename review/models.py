from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey('review.Company', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('authentication.User', on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=64)
    company_id = models.IntegerField(unique=True)
    website = models.URLField(null=True, blank=True)
