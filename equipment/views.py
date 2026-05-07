from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import ClinicEquipment

# Create your views here.
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'administrator'


class EquipmentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClinicEquipment
    template_name = 'equipment/list.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    queryset = ClinicEquipment.objects.select_related('category')


class EquipmentDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = ClinicEquipment
    template_name = 'equipment/list.html'
    context_object_name = 'item'


class EquipmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClinicEquipment
    template_name = 'equipment/list.html'
    fields = ['category', 'name', 'instruction', 'warranty_period', 'certificate', 'price']
    success_url = reverse_lazy('equipment:list')
