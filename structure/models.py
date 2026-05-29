from django.db import models


class Department(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название подразделения')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Связанное подразделение', related_name='children')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:

        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent_id'],
                name='unique_department_per_parent'
            )
        ]

    def __str__(self):
        return self.name


class Employee(models.Model):

    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Подразделение', related_name='employees')
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    position = models.CharField(max_length=200, verbose_name = 'Должность')
    hired_at = models.DateField(null=True, blank=True, verbose_name='Дата трудоустройства')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:

        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name
