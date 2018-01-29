from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
	if instance and created:
		instance.profile = Profile.objects.create(user=instance)

@receiver(post_delete, sender=User)
def auto_delete_avatar_on_delete(sender, instance, **kwargs):
	try:
		if instance.avatar:
			os.remove(instance.avatar.path)
	except OSError:
		pass