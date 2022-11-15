from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
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


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='content/charts.html')
line_chart_json = LineChartJSONView.as_view()
