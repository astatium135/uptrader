from django.db import models
from django.core.exceptions import ValidationError

class Menu(models.Model):
    #id создаётся автоматически, лезть в процесс не надо
    parent = models.ForeignKey(
        "Menu", 
        on_delete=models.CASCADE, 
        verbose_name="родительский элемент",
        blank=True, null=True
        )
    label = models.TextField(verbose_name="подпись")
    link = models.TextField(verbose_name="ссылка", blank=True, null=True) #сценарий для родительского элемента меню

    def save(self, *args, **kwargs):
        if self. parent and not self.link:
            raise ValidationError("у не-корневых пунктов меню ссылка не может быть пустой")
        super().save(args, kwargs)
    
    def __str__(self):
        return self.label
    
    class Meta:
        verbose_name = verbose_name_plural = "меню"