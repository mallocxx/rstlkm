from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import ChangeLog
from locations.models import Building, Apartment
from surveys.models import Visit, Survey


def capture_diff(old: dict, new: dict) -> dict:
	diff = {}
	for k in new.keys():
		if old.get(k) != new.get(k):
			diff[k] = {"old": old.get(k), "new": new.get(k)}
	return diff

@receiver(pre_save, sender=Building)
@receiver(pre_save, sender=Apartment)
@receiver(pre_save, sender=Visit)
@receiver(pre_save, sender=Survey)
def log_changes(sender, instance, **kwargs):
	if not instance.pk:
		return
	try:
		old_instance = sender.objects.get(pk=instance.pk)
	except sender.DoesNotExist:
		return
	old = model_to_dict(old_instance)
	new = model_to_dict(instance)
	diff = capture_diff(old, new)
	if diff:
		ChangeLog.objects.create(
			entity_type=sender.__name__,
			entity_id=instance.pk,
			changed_by=getattr(getattr(instance, 'visitor', None), 'id', None) or None,
			diff=diff,
		)
