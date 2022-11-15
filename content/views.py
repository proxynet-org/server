from django.views.generic import TemplateView
from chartjs.views.columns import BaseColumnsHighChartsView
from django.shortcuts import render
from users.models import User
from .models import Message

# Render users.html


def UserListView(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'content/users.html', context)


def UserDetailView(request, pk):
    context = {
        'messages': Message.objects.filter(user=pk),
    }
    return render(request, 'content/user_messages.html', context)


class LineChartJSONView(BaseColumnsHighChartsView):

    def get_title(self):
        return "My Awesome Chart"

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_yAxis(self):
        return super().get_yAxis()

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", ]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35], ]


line_chart = TemplateView.as_view(template_name='content/charts.html')
line_chart_json = LineChartJSONView.as_view()
