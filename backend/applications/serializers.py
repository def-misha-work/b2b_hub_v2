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
    class Meta:
        model = Applications
        fields = (
            "tg_user",
            "cost",
            "target_date",
            "inn_payer",
            "inn_recipient",
        )
