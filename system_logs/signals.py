from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from tanks.models import Tank
from .models import SystemLog

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    if created:
        SystemLog.objects.create(
            log_type='USER_CREATED',
            level='SUCCESS',
            message=f'Usuario "{instance.username}" creado',
            user=instance,
            metadata={'username': instance.username}
        )


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    SystemLog.objects.create(
        log_type='USER_DELETED',
        level='WARNING',
        message=f'Usuario "{instance.username}" eliminado',
        metadata={'username': instance.username}
    )


@receiver(post_save, sender=Tank)
def log_tank_save(sender, instance, created, **kwargs):
    if created:
        SystemLog.objects.create(
            log_type='TANK_CREATED',
            level='INFO',
            message=f'Tanque "{instance.name}" creado por {instance.owner.username}',
            user=instance.owner,
            metadata={
                'tank_name': instance.name,
                'capacity': instance.capacity_liters,
                'owner': instance.owner.username
            }
        )


@receiver(post_delete, sender=Tank)
def log_tank_delete(sender, instance, **kwargs):
    owner_username = instance.owner.username if instance.owner else 'desconocido'
    SystemLog.objects.create(
        log_type='TANK_DELETED',
        level='WARNING',
        message=f'Tanque "{instance.name}" del usuario "{owner_username}" eliminado',
        user=instance.owner if instance.owner else None,
        metadata={
            'tank_name': instance.name,
            'owner': owner_username
        }
    )