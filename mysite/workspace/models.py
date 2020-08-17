from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals


def create_ForUser(sender, instance, created, **kwargs):
    ForUser.objects.create(user=instance)


class Outlet(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название книги")
    view = models.IntegerField(verbose_name="Кол.Просмотров")
    working = models.BooleanField(default=True, verbose_name="Состояние")

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        result = self.name
        return result


class HistoryGiveUser(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    give_outlet = models.ForeignKey(Outlet, on_delete=models.SET_NULL, null=True, verbose_name="Книга")
    give_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Оператор")

    class Meta:
        verbose_name = 'Просмотренная Книга'
        verbose_name_plural = 'Просмотренные Книги'

    def __str__(self):
        result = str(self.date_time) + ' Outlet: ' + str(self.give_outlet) + ' User: ' + str(self.give_user)
        return result


class Task(models.Model):
    date_time = models.DateTimeField(verbose_name="Дата")
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Оператор")
    outlet = models.ForeignKey(Outlet, on_delete=models.SET_NULL, null=True, verbose_name="Книга")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Поставленная задача'
        verbose_name_plural = 'Поставленные задачи'

    def __str__(self):
        result = str(self.date_time) + ' Operator: ' + str(self.operator) + ' Outlet: ' + str(self.outlet)
        return result


class Refund(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    date_achieve = models.DateField(verbose_name="Дата выполнения")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Оператор")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        result = str(self.date) + ' Date achieve: ' + str(self.date_achieve) + ' User: ' + str(self.user)
        return result


class HelpTable(models.Model):
    outlet_update = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Переключатель'
        verbose_name_plural = 'Переключатели'

    def __str__(self):
        result = 'Состояние переключателя'
        return result


class ForUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Оператор')
    refund = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Расширение для возврата'
        verbose_name_plural = 'Расширение для возвратов'

    def __str__(self):
        result = self.user.username
        return result


class ForFile(models.Model):
    app_for_time = models.FileField(upload_to='downloads/')

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        result = 'Программа'
        return result


signals.post_save.connect(create_ForUser, sender=User)
