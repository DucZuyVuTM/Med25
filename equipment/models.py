from django.db import models

# Create your models here.
class ClinicEquipmentCategory(models.Model):
    """Medical equipment catalog (e.g., diagnostic imaging, surgical, ...)."""

    description = models.TextField(verbose_name='Category description')

    class Meta:
        verbose_name = 'Clinic Equipment Category'
        verbose_name_plural = 'Clinic Equipment Categories'

    def __str__(self):
        return f'Equipment Category #{self.pk}: {self.description[:60]}'


class ClinicEquipment(models.Model):
    """Specific medical equipment of the clinic."""

    category = models.ForeignKey(
        ClinicEquipmentCategory,
        on_delete=models.PROTECT,
        related_name='equipment_items',
        verbose_name='Category',
    )
    name = models.CharField(max_length=50, verbose_name='Equipment name')
    instruction = models.TextField(verbose_name='Instruction')
    warranty_period = models.DateTimeField(verbose_name='Warranty period')
    certificate = models.TextField(verbose_name='Certificate / License')
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Price')

    class Meta:
        verbose_name = 'Clinic Equipment'
        verbose_name_plural = 'Clinic Equipments'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.category})'
