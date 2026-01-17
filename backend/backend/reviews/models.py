from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from backend import users


# Create your models here.
class Review(models.Model):

    SCORE = (
        (1, 'Poor'),
        (2, 'Subpar'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    donor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='review_received')
    reviewer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='review_given')
    rating = models.IntegerField(_('rating'), choices=SCORE)
    comment = models.TextField(_('comment'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.comment + " by @" + self.reviewer
