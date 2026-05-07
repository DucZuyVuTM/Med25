from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Schedule

# Create your views here.
class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'scheduling/list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = Schedule.objects.select_related('administrator__employee')
        # Doctors and patients only see the schedule relevant to them.
        if user.role == 'doctor':
            qs = qs.filter(receptions__doctor__employee__user=user).distinct()
        elif user.role == 'patient':
            qs = qs.filter(receptions__patient__user=user).distinct()
        return qs


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule
    template_name = 'scheduling/detail.html'
    context_object_name = 'schedule'


class ScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Schedule
    template_name = 'scheduling/list.html'
    fields = ['reception_start_time', 'reception_end_time', 'reception_place']
    success_url = reverse_lazy('scheduling:list')

    def test_func(self):
        return self.request.user.role == 'administrator'

    def form_valid(self, form):
        form.instance.administrator = self.request.user.administrator_profile
        return super().form_valid(form)
