from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    # address1 = models.CharField(blank=True, max_length = 200)
    # address2 = models.CharField(blank=True, max_length = 200)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username