from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        abstract = True


class TelegamUsers(TimestampMixin, models.Model):
    tg_username = models.CharField(
        verbose_name="Никнеим автора заявки в tg",
        max_length=512,
        unique=True
    )
    tg_user_id = models.TextField(
        verbose_name="ID автора заявки в tg",
        unique=True
    )
    name = models.CharField(
        verbose_name="Имя автора заявки в tg",
        max_length=512,
        default=None,
        blank=True,
        null=True,
    )
    lastname = models.CharField(
        verbose_name="Фамилия автора заявки в tg",
        max_length=512,
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Клиенты"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.tg_username


class TelegramGroup(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название группы"
    )
    users = models.ManyToManyField(
        TelegamUsers,
        related_name='groups',
        verbose_name="Пользователи"
    )

    class Meta:
        verbose_name = "Группы клиентов"
        verbose_name_plural = "Группы клиентов"

    def __str__(self):
        return self.name


class MessageTemplate(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    groups = models.ManyToManyField(
        TelegramGroup,
        related_name='message_templates'
    )

    class Meta:
        verbose_name = "Рассылки"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.title


class MessageLog(models.Model):
    template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    group = models.ForeignKey(
        TelegramGroup,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    status_code = models.IntegerField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "История рассылок"
        verbose_name_plural = "История рассылок"

    def __str__(self):
        log_message = (
            f"Log for {self.template.title} "
            f"to {self.group.name} "
            f"at {self.timestamp}"
        )
        return log_message


class UserMessageLog(models.Model):
    message_log = models.ForeignKey(
        MessageLog,
        on_delete=models.CASCADE,
        related_name='user_logs'
    )
    user = models.ForeignKey(
        TelegamUsers,
        on_delete=models.CASCADE,
        related_name='message_logs'
    )
    status_code = models.IntegerField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.user.name} at {self.timestamp}"


class CompaniesPayer(TimestampMixin, models.Model):
    tg_user = models.ForeignKey(
        TelegamUsers,
        on_delete=models.CASCADE,
        verbose_name="Владелец компании",
        default=None,
    )
    company_name_payer = models.CharField(
        verbose_name="Название компании плательщика",
        max_length=512,
        default=None,
        null=True
    )
    company_inn_payer = models.CharField(
        verbose_name="ИНН плательщика 10 цифр",
        max_length=10,
        unique=True
    )

    class Meta:
        verbose_name = "Компания плательщик"
        verbose_name_plural = "Компании плательщики"

    def __str__(self):
        if self.company_name_payer:
            return self.company_name_payer
        else:
            return self.company_inn_payer


class CompaniesRecipient(TimestampMixin, models.Model):
    tg_user = models.ForeignKey(
        TelegamUsers,
        on_delete=models.CASCADE,
        verbose_name="Владелец компании",
        default=None,
    )
    company_name_recipient = models.CharField(
        verbose_name="Название компании получателя",
        max_length=512,
        default=None,
        null=True
    )
    company_inn_recipient = models.CharField(
        verbose_name="ИНН получателя 12 цифр",
        max_length=12,
        unique=True
    )

    class Meta:
        verbose_name = "Компания получатель"
        verbose_name_plural = "Компании получатели"

    def __str__(self):
        if self.company_name_recipient:
            return self.company_name_recipient
        else:
            return self.company_inn_recipient


class Applications(TimestampMixin, models.Model):
    STATUS_CHOICES = [
        ("Новая", "Новая"),
        ("В работе", "В работе"),
        ("Счёт в оплате", "Счёт в оплате"),
        ("Выполнена", "Выполнена"),
    ]
    tg_user = models.ForeignKey(
        TelegamUsers,
        on_delete=models.CASCADE,
        verbose_name="Автор заявки",
    )
    cost = models.IntegerField(
        verbose_name="Сумма заявки",
        validators=[MinValueValidator(1), MaxValueValidator(10000000)]
    )
    target_date = models.DateField(
        verbose_name="Дата исполнения заявки"
    )
    inn_payer = models.ForeignKey(
        CompaniesPayer,
        related_name="applications_as_payer",
        on_delete=models.CASCADE,
        verbose_name="Название или ИНН получателя",
    )
    inn_recipient = models.ForeignKey(
        CompaniesRecipient,
        related_name="applications_as_recipient",
        on_delete=models.CASCADE,
        verbose_name="Название или ИНН плательщика",
    )
    app_status = models.CharField(
        verbose_name="Статус заявки",
        max_length=200,
        choices=STATUS_CHOICES,
        default="Новая"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        default="",
        verbose_name="Комментарии к заявке",
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка от пользователя: {self.tg_user}"
