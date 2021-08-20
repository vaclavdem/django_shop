from rest_framework import serializers

from delivery.models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Жалоба"""

    class Meta:
        model = Report
        fields = ("email", "order", "comment", "id")


class ReportUserSerializer(serializers.ModelSerializer):
    """Добавление жалобы"""

    class Meta:
        model = Report
        fields = ("email", "comment")