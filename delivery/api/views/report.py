from rest_framework import generics, permissions

from delivery.models import Order, Report

from delivery.api.serializers.report import ReportSerializer, ReportUserSerializer

from delivery.service.permissions import IsModeratorUser

from delivery.service.tasks import send_email

from datetime import datetime
import time


class ReportsView(generics.ListAPIView):
    """список жалоб"""
    serializer_class = ReportSerializer
    permission_classes = (IsModeratorUser,)
    queryset = Report.objects.all()


class ReportDestroyView(generics.RetrieveDestroyAPIView):
    """Удаление жалобы"""
    permission_classes = (IsModeratorUser,)
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportCreateView(generics.CreateAPIView):
    """Добавление жалоб"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportUserSerializer

    def perform_create(self, serializer):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        now = time.mktime(datetime.now().timetuple())
        if now - order.ddelivered_at < 300:
            serializer.save(order=order)
            send_email("Информирование", "С вашего устройства создали жалобу", self.request.data.get("email"))
        else:
            pass