from django.db import models

from user.models import User

class Startup(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status_choices = [
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('closed', 'Closed')
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    description = models.TextField()
    start_date = models.DateField(null=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    founder = models.CharField(max_length=100, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    investors = models.ManyToManyField(User, related_name='investments', blank=True)
    rating = models.IntegerField(default=5)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_startups')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        """Meta options."""

        ordering = ["created_at"]

    @property
    def investors_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.first_name + key.last_name for key in self.investors.all()]