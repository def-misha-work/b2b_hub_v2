from rest_framework import serializers

from applications.models import (
    Applications,
    CompaniesPayer,
    CompaniesRecipient,
    TelegamUsers,
)


class TelegamUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegamUsers
        fields = (
            "tg_username",
            "tg_user_id",
            "name",
            "lastname",
        )


class CompaniesPayerSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesPayer
        fields = (
            "tg_user_id",
            "company_name_payer",
            "company_inn_payer",
        )

    def get_tg_user_id(self, obj):
        return obj.tg_user.tg_user_id


class CompaniesPostUpdatePayerSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.CharField(max_length=255)
    tg_user_id_display = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesPayer
        fields = (
            "tg_user_id",
            "tg_user_id_display",
            "company_name_payer",
            "company_inn_payer",
        )

    def get_tg_user_id_display(self, obj):
        return obj.tg_user.tg_user_id

    def create(self, validated_data):
        tg_user_id = validated_data.pop('tg_user_id')
        try:
            tg_user = TelegamUsers.objects.get(tg_user_id=tg_user_id)
        except TelegamUsers.DoesNotExist:
            raise serializers.ValidationError(
                "Нет юзера с таким id."
            )

        return CompaniesPayer.objects.create(
            tg_user=tg_user,
            **validated_data
        )

    def update(self, instance, validated_data):
        tg_user_id = validated_data.pop('tg_user_id', None)

        if tg_user_id is not None:
            try:
                tg_user = TelegamUsers.objects.get(
                    tg_user_id=tg_user_id
                )
                instance.tg_user = tg_user
            except TelegamUsers.DoesNotExist:
                raise serializers.ValidationError(
                    "Нет юзера с таким id."
                )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CompaniesRecipientSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesRecipient
        fields = (
            "tg_user_id",
            "company_name_recipient",
            "company_inn_recipient",
        )

    def get_tg_user_id(self, obj):
        return obj.tg_user.tg_user_id


class CompaniesPostUpdateRecipientSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.CharField(max_length=255)
    tg_user_id_display = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesRecipient
        fields = (
            "tg_user_id",
            "tg_user_id_display",
            "company_name_recipient",
            "company_inn_recipient",
        )

    def get_tg_user_id_display(self, obj):
        return obj.tg_user.tg_user_id

    def create(self, validated_data):
        tg_user_id = validated_data.pop('tg_user_id')
        try:
            tg_user = TelegamUsers.objects.get(tg_user_id=tg_user_id)
        except TelegamUsers.DoesNotExist:
            raise serializers.ValidationError(
                "Нет юзера с таким id."
            )

        return CompaniesRecipient.objects.create(
            tg_user=tg_user,
            **validated_data
        )

    def update(self, instance, validated_data):
        tg_user_id = validated_data.pop('tg_user_id', None)

        if tg_user_id is not None:
            try:
                tg_user = TelegamUsers.objects.get(
                    tg_user_id=tg_user_id
                )
                instance.tg_user = tg_user
            except TelegamUsers.DoesNotExist:
                raise serializers.ValidationError(
                    "Нет юзера с таким id."
                )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ApplicationsSerializer(serializers.ModelSerializer):

    tg_user_id = serializers.SerializerMethodField()
    inn_payer = serializers.SerializerMethodField()
    inn_recipient = serializers.SerializerMethodField()
    target_date = serializers.DateField(
        format="%d.%m.%y",
        input_formats=['%d.%m.%y', 'iso-8601']
    )

    class Meta:
        model = Applications
        fields = (
            "id",
            "tg_user_id",
            "cost",
            "target_date",
            "inn_payer",
            "inn_recipient",
            "app_status",
        )
        read_only_fields = ('id',)

    def get_tg_user_id(self, obj):
        return obj.tg_user.tg_user_id

    def get_inn_payer(self, obj):
        return obj.inn_payer.company_inn_payer

    def get_inn_recipient(self, obj):
        return obj.inn_recipient.company_inn_recipient


class ApplicationsPostUpdateSerializer(serializers.ModelSerializer):

    tg_user_id = serializers.CharField(max_length=255)
    target_date = serializers.DateField(
        format="%d.%m.%y",
        input_formats=['%d.%m.%y', '%d.%m.%Y', 'iso-8601']
    )
    inn_payer = serializers.CharField(write_only=True)
    inn_recipient = serializers.CharField(write_only=True)

    # поля для response
    tg_user_id_display = serializers.SerializerMethodField()
    inn_payer_display = serializers.SerializerMethodField()
    inn_recipient_display = serializers.SerializerMethodField()

    class Meta:
        model = Applications
        fields = (
            "id",
            "tg_user_id",
            "cost",
            "target_date",
            "inn_payer",
            "inn_recipient",
            "tg_user_id_display",
            "inn_payer_display",
            "inn_recipient_display",
            "app_status"
        )
        read_only_fields = ('id',)

    def get_tg_user_id_display(self, obj):
        return obj.tg_user.tg_user_id

    def get_inn_payer_display(self, obj):
        return obj.inn_payer.company_inn_payer

    def get_inn_recipient_display(self, obj):
        return obj.inn_recipient.company_inn_recipient

    def create(self, validated_data):
        tg_user_id = validated_data.pop('tg_user_id')
        try:
            tg_user = TelegamUsers.objects.get(tg_user_id=tg_user_id)
        except TelegamUsers.DoesNotExist:
            raise serializers.ValidationError(
                "Нет юзера с таким id."
            )

        inn_payer = validated_data.pop('inn_payer')
        try:
            inn_payer = CompaniesPayer.objects.get(company_inn_payer=inn_payer)
        except CompaniesPayer.DoesNotExist:
            raise serializers.ValidationError(
                "Нет компании плательщика с таким ИНН."
            )

        inn_recipient = validated_data.pop('inn_recipient')
        try:
            inn_recipient = CompaniesRecipient.objects.get(
                company_inn_recipient=inn_recipient
            )
        except CompaniesRecipient.DoesNotExist:
            raise serializers.ValidationError(
                "Нет компании получателя с таким ИНН."
            )

        return Applications.objects.create(
            tg_user=tg_user,
            inn_payer=inn_payer,
            inn_recipient=inn_recipient,
            **validated_data
        )

    def update(self, instance, validated_data):
        tg_user_id = validated_data.pop('tg_user_id', None)
        inn_payer_data = validated_data.pop('inn_payer', None)
        inn_recipient_data = validated_data.pop('inn_recipient', None)

        if tg_user_id is not None:
            try:
                tg_user = TelegamUsers.objects.get(tg_user_id=tg_user_id)
                instance.tg_user = tg_user
            except TelegamUsers.DoesNotExist:
                raise serializers.ValidationError(
                    "Нет юзера с таким id."
                )

        if inn_payer_data is not None:
            try:
                inn_payer = CompaniesPayer.objects.get(
                    company_inn_payer=inn_payer_data
                )
                instance.inn_payer = inn_payer
            except CompaniesPayer.DoesNotExist:
                raise serializers.ValidationError(
                    "Нет компании плательщика с таким ИНН."
                )

        if inn_recipient_data is not None:
            try:
                inn_recipient = CompaniesRecipient.objects.get(
                    company_inn_recipient=inn_recipient_data
                )
                instance.inn_recipient = inn_recipient
            except CompaniesRecipient.DoesNotExist:
                raise serializers.ValidationError(
                    "Нет компании получателя с таким ИНН."
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
