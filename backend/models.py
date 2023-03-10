from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

REASON_TYPE = [
    ('wedding', 'Свадьба'),
    ('birthday', 'День рождения'),
    ('no_reason', 'Без повода'),
]

COLOR_HYE = [
    ('pink', 'Розовая'),
    ('white', 'Белая'),
    ('red', 'Красная'),
    ('yellow', 'Жёлтая'),
    ('purple', 'Фиолетовая'),
]

DELIVERY_TIME_CHOICES = [
    ('ASAP', 'Как можно скорее'),
    ('10:00-12:00', '10:00-12:00'),
    ('12:00-14:00', '12:00-14:00'),
    ('14:00-16:00', '14:00-16:00'),
    ('16:00-18:00', '16:00-18:00'),
    ('18:00-20:00', '18:00-20:00'),
]

CONSULTATION_STATUS = [
    ('waiting', 'Ожидает'),
    ('in progress', 'В работе'),
    ('rejection', 'Отказ от заказа'),
    ('done', 'Заказ оформлен'),
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
    color_hye = models.CharField(
        'Цветовая гамма',
        choices=COLOR_HYE,
        max_length=15,
        blank=True,
        null=True,
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
    address = models.CharField(
        'Адрес доставки',
        max_length=100,
    )
    delivery_date = models.DateField(
        'Дата доставки',
        default=timezone.now,
    )
    delivery_time = models.CharField(
        'Время доставки',
        max_length=15,
        choices=DELIVERY_TIME_CHOICES,
        default='ASAP',
    )
    is_payed = models.BooleanField(
        'Оплачено',
        default=False,
        db_index=True,
    )
    is_delivered = models.BooleanField(
        'Выполнен',
        default=False,
        db_index=True,
    )
    yookassa_payment_id = models.CharField(
        'ID платежа Юкасса',
        max_length=80,
        blank=True
    )
    created_at = models.DateTimeField(
        'Когда создан заказ',
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.bouquet} для {self.client_name}'


class Consultation(models.Model):
    status = models.CharField(
        'Статус работы',
        max_length=20,
        choices=CONSULTATION_STATUS,
        default='waiting',
        db_index=True,
    )
    order = models.ForeignKey(
        'Order',
        related_name='orders',
        verbose_name='Заказ',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
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
    created_at = models.DateTimeField(
        'Когда создан запрос',
        default=timezone.now,
        db_index=True,
    )
    comment = models.TextField(
        'Заметки по клиенту',
        blank=True,
    )

    def clean(self):
        if self.status == 'rejection' and not self.comment:
            raise ValidationError("Комментарий не заполнен")
        if self.status == 'done' and not self.order:
            raise ValidationError("Не указан заказ")

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f'{self.client_name} в {self.created_at}'


class ConsultationSummary(Consultation):
    class Meta:
        proxy = True
        verbose_name = 'Статистика консультации'
        verbose_name_plural = 'Статистика консультаций'


class OrderSummary(Order):
    class Meta:
        proxy = True
        verbose_name = 'Статистика заказа'
        verbose_name_plural = 'Статистика заказов'