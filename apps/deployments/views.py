from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import DeployForm
from django.urls import reverse_lazy

# Create your views here.
class DeployView(FormView):
    template_name = 'deployments/deploy.html'
    form_class = DeployForm
    success_url = reverse_lazy('packages:list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.deploy()
        return super(DeployView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(DeployView, self).get_form_kwargs()
        if 'package_id' not in kwargs:
            kwargs['package_id'] = self.kwargs['package_id']
        return kwargs
    
    