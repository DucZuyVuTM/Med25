from django.db import models

# Create your models here.
class Document(models.Model):
    """The document, created by the administrator, which is attached to the reception."""
 
    administrator = models.ForeignKey(
        'accounts.Administrator',
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name='Administrator',
    )
    content = models.TextField(verbose_name='Document content')
    formation_date = models.DateField(verbose_name='Formation date')
 
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-formation_date']
 
    def __str__(self):
        return f'Document #{self.pk} - {self.formation_date}'
