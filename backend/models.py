from django.db import models
from django.utils import timezone

REASON_TYPE = [
    ('wedding', 'Свадьба'),
    ('birthday', 'День рождения'),
    ('no_reason', 'Без повода'),
]


class Bouquet(models.Model):
    title = models.CharField(
        'Название',
        max_length=50,
        db_index=True,
    )
    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
    )
    reason = models.CharField(
        'Событие',
        max_length=20,
        choices=REASON_TYPE,
        default='no_reason',
        db_index=True,
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    composition = models.TextField(
        'Состав букета',
        blank=True,
    )
    height = models.IntegerField(
        'Высота',
        null=True,
        blank=True,
    )
    width = models.IntegerField(
        'Ширина',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        'Картинка',
        blank=True,
    )

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.title


class Order(models.Model):
    bouquet = models.ForeignKey(
        'Bouquet',
        related_name='orders',
        verbose_name='Букет',
        on_delete=models.PROTECT,
    )
    client_name = models.CharField(
        'ФИО клиента',
        max_length=200,
        db_index=True
    )
    phonenumber = models.CharField(
        'Номер клиента',
        max_length=20,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.bouquet} для {self.client_name}'


class Consultation(models.Model):
    client_name = models.CharField(
        'ФИО клиента',
        max_length=200,
        db_index=True
    )
    phonenumber = models.CharField(
        'Номер клиента',
        max_length=20,
    )
    created_at = models.DateTimeField(
        'Когда создан запрос',
        default=timezone.now,
        db_index=True,
    )
    closed = models.BooleanField(
        'Консультация проведена',
        default=False,
        db_index=True,
    )
    comment = models.TextField(
        'Заметки по клиенту',
        blank=True,
    )
