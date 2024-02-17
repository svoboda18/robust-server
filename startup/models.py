from django.db import models

from user.models import User

class Startup(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status_choices = [
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('closed', 'Closed'),
        ('ai-approved','AiApproved'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, blank=True)
    description = models.TextField()
    start_date = models.DateField(null=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    founder = models.CharField(max_length=100, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    investments_total = models.FloatField(blank=True, null=True)
    mentors = models.ManyToManyField(User, related_name='startups', blank=True)
    rating = models.IntegerField(default=5)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_startups', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        """Meta options."""

        ordering = ["created_at"]

    @property
    def investors_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [key.first_name + key.last_name for key in self.investors.all()]
    
class StartupAi(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='created_startups')
    latitude = models.FloatField()
    longitude = models.FloatField()
    labels = models.CharField(max_length=255)
    age_first_funding_year = models.IntegerField()
    age_last_funding_year = models.IntegerField()
    age_first_milestone_year = models.IntegerField()
    age_last_milestone_year = models.IntegerField()
    relationships = models.IntegerField()
    funding_rounds = models.IntegerField()
    funding_total_usd = models.FloatField()
    milestones = models.IntegerField()
    is_CA = models.BooleanField()
    is_NY = models.BooleanField()
    is_MA = models.BooleanField()
    is_TX = models.BooleanField()
    is_otherstate = models.BooleanField()
    category_code = models.CharField(max_length=255)
    is_software = models.BooleanField()
    is_web = models.BooleanField()
    is_mobile = models.BooleanField()
    is_enterprise = models.BooleanField()
    is_advertising = models.BooleanField()
    is_gamesvideo = models.BooleanField()
    is_ecommerce = models.BooleanField()
    is_biotech = models.BooleanField()
    is_consulting = models.BooleanField()
    is_othercategory = models.BooleanField()
    has_VC = models.BooleanField()
    has_angel = models.BooleanField()
    has_roundA = models.BooleanField()
    has_roundB = models.BooleanField()
    has_roundC = models.BooleanField()
    has_roundD = models.BooleanField()
    avg_participants = models.FloatField()
    is_top500 = models.BooleanField()

    def __str__(self):
        return f'{self.labels} - {self.category_code}'


    
    