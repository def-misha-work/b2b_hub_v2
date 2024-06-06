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
    class Meta:
        model = CompaniesPayer
        fields = (
            "company_name",
            "company_inn",
        )


class CompaniesRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompaniesRecipient
        fields = (
            "company_name",
            "company_inn",
        )


class ApplicationsSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.IntegerField(write_only=True)
    target_date = serializers.DateField(
        format="%d.%m.%y",
        input_formats=['%d.%m.%y', 'iso-8601']
    )
    inn_payer = serializers.IntegerField(write_only=True)
    inn_recipient = serializers.IntegerField(write_only=True)
    tg_user = serializers.SerializerMethodField()
    payer = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()

    class Meta:
        model = Applications
        fields = (
            "id",
            "tg_user_id",
            "cost",
            "target_date",
            "inn_payer",
            "inn_recipient",
            "tg_user",
            "payer",
            "recipient",
        )
        read_only_fields = ('id',)

    def get_tg_user(self, obj):
        return obj.tg_user.tg_user_id

    def get_payer(self, obj):
        return obj.inn_payer.company_inn

    def get_recipient(self, obj):
        return obj.inn_recipient.company_inn

    def create(self, validated_data):
        tg_user_id = validated_data.pop('tg_user_id')
        try:
            tg_user = TelegamUsers.objects.get(tg_user_id=tg_user_id)
        except TelegamUsers.DoesNotExist:
            raise serializers.ValidationError("Нет юзера с таким id.")

        inn_payer = validated_data.pop('inn_payer')
        try:
            inn_payer = CompaniesPayer.objects.get(company_inn=inn_payer)
        except CompaniesPayer.DoesNotExist:
            raise serializers.ValidationError(
                "Нет компании плательщика с таким ИНН."
            )

        inn_recipient = validated_data.pop('inn_recipient')
        try:
            inn_recipient = CompaniesRecipient.objects.get(
                company_inn=inn_recipient
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
