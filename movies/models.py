from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


# Create your models here.
class Collection(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    collection_user = models.ForeignKey(User, related_name="collection_user",
                                        on_delete=models.CASCADE)
    title = models.CharField(max_length=100,
                             validators=[MinLengthValidator(4)])
    description = models.TextField(validators=[MinLengthValidator(10)])
    movies = models.JSONField()
    created_by = models.IntegerField(unique=False)
    updated_by = models.IntegerField(unique=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(blank=True, null=True)
    is_active = models.IntegerField(default=1)

    def __repr__(self) -> str:
        resp = "collection_uuid is "+str(self.id)
        return resp
