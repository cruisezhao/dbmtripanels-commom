from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .forms import *

class InterfaceCreateView(View):
    parent_model = None
    parent_field = None
    model = None
    form = None
    model_form = None
    template_name = None

    def get(self, request, uuid):

        parent = get_object_or_404(self.parent_model, uuid=uuid)
        form = self.form(parent, initial=request.GET)

        return render(request, self.template_name, {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': parent.get_absolute_url(),
        })

    def post(self, request, uuid):

        parent = get_object_or_404(self.parent_model, uuid=uuid)

        form = self.form(parent, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            component_data = {
                    self.parent_field: parent.pk,
                }
            # Replace objects with their primary key to keep component_form.clean() happy
            for k, v in data.items():
                if hasattr(v, 'pk'):
                    component_data[k] = v.pk
                else:
                    component_data[k] = v
            if data['type'] == 'Rack':
                self.model_form = InterfaceRackForm
            elif data['type'] == 'Network':
                self.model_form = InterfaceNetworkForm
            else:
                self.model_form = InterfaceForm

            component_form = self.model_form(component_data)
            if component_form.is_valid():
                component_form.save()
                if not component_form.errors:
                    return redirect(parent.get_detail_url())

        return render(request, self.template_name, {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': parent.get_absolute_url(),
        })






