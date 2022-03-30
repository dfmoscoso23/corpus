from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# class User2(AbstractUser):
#   @receiver(post_save, sender=User)
#   def user_to_inactive(sender, instance, created, update_fields, **kwargs):
#       if created:
#           instance.is_active = False

# Create your models here.
class Profile(models.Model):
	estudiante = 1
	graduado = 2
	investigador = 3
	ROLE_CHOICES = (
		(estudiante, 'Estudiante'),
		(graduado, 'Graduado'),
		(investigador, 'Investigador'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=30, blank=True, null=True)
	birthdate = models.DateField(null=True, blank=True)
	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
	bio = models.CharField(max_length=350, blank=True, null=True)

	def __str__(self):  # __unicode__ for Python 2
		return self.user.username

	@receiver(post_save, sender=User)
	def create_or_update_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)
			#instance.profile.save()