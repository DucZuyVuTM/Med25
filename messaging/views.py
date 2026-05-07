from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django import forms
from .models import Email, Message

# Create your views here.
class InboxView(LoginRequiredMixin, ListView):
    model = Email
    template_name = 'messaging/inbox.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == 'administrator':
            return Email.objects.filter(
                administrator__employee__user=user
            ).select_related('patient')
        elif user.role == 'patient':
            return Email.objects.filter(
                patient__user=user
            ).select_related('administrator__employee')
        return Email.objects.none()


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Message content'
    )


class ThreadView(LoginRequiredMixin, DetailView):
    model = Email
    template_name = 'messaging/thread.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            sender_type = 'admin' if request.user.role == 'administrator' else 'patient'
            from django.utils import timezone
            now = timezone.now()
            Message.objects.create(
                email=thread,
                content=form.cleaned_data['content'],
                send_date=now.date(),
                send_time=now.time(),
                sender_type=sender_type,
            )
        return self.get(request, *args, **kwargs)
