from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя пользователя")
    email = models.EmailField(null=False, verbose_name="e-mail")
    create_date = models.DateTimeField(auto_now_add=True,  verbose_name="Дата регистрации")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['create_date', 'name']

    def __str__(self):
        return self.name


class Meeting(models.Model):
    date_meet = models.DateField(verbose_name="Дата встречи")
    time_start = models.TimeField(verbose_name="Время начала встречи")
    time_end = models.TimeField(verbose_name="Время окончания встречи")
    quantity = models.IntegerField(verbose_name="Участников")
    option1 = models.BooleanField(default=0, verbose_name="Опция 1")
    option2 = models.BooleanField(default=0, verbose_name="Опция 2")
    status = models.IntegerField(default=0, verbose_name="Статус")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'
        ordering = ['date_meet', 'time_start', 'status']

    def __str__(self):
        return f"Встреча {self.pk}"


class Rooms(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    volume = models.IntegerField(null=False, verbose_name="Кол-во мест")
    option1 = models.BooleanField(default=0, verbose_name="Опция 1")
    option2 = models.BooleanField(default=0, verbose_name="Опция 2")
    plan = models.JSONField(null=True)

    class Meta:
        verbose_name = 'Переговорка'
        verbose_name_plural = 'Переговорки'
        ordering = ['name', 'volume', 'option1', 'option2']

    def __str__(self):
        return f"Переговорка {self.pk}"


class Param(models.Model):
    startworktime = models.TimeField(null=True, verbose_name="Начало рабочего дня")
    endtworktime = models.TimeField(null=True, verbose_name="Конец рабочего дня")
    timestap = models.IntegerField(null=True, verbose_name="Шаг планирования в минутах")
    numofroom = models.IntegerField(null=True, verbose_name="Количество комнат")
    roomlist = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'
        ordering = ['startworktime', 'endtworktime', 'timestap', 'user', 'created_at']

    def __str__(self):
        return f"Параметр {self.pk}"


