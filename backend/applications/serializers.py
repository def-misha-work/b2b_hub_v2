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
    tg_user_id = serializers.IntegerField()
    target_date = serializers.DateField(
        format="%d.%m.%y",
        input_formats=['%d.%m.%y', 'iso-8601']
    )
    inn_payer = serializers.IntegerField()
    inn_recipient = serializers.IntegerField()

    class Meta:
        model = Applications
        fields = (
            "id",
            "tg_user_id",
            "cost",
            "target_date",
            "inn_payer",
            "inn_recipient",
        )
        read_only_fields = ('id',)

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
