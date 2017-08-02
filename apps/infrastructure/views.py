from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .forms import *
from copy import deepcopy

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
            new_components = []
            data = deepcopy(form.cleaned_data)

            if data['type'] == 'Rack':
                self.model_form = InterfaceRackForm
            elif data['type'] == 'Network':
                self.model_form = InterfaceNetworkForm
            else:
                self.model_form = InterfaceForm

            name_tag_index = zip(form.cleaned_data['name_pattern'], form.cleaned_data['tag_pattern'], form.cleaned_data['index_pattern'])

            for name, tag, index in name_tag_index:
                component_data = {
                    self.parent_field: parent.pk,
                    'name': name,
                    'tag': tag,
                    'index': index,
                }
                # Replace objects with their primary key to keep component_form.clean() happy
                for k, v in data.items():
                    if hasattr(v, 'pk'):
                        component_data[k] = v.pk
                    else:
                        component_data[k] = v
                component_form = self.model_form(component_data)
                if component_form.is_valid():
                    new_components.append(component_form.save(commit=False))
                else:
                    for field, errors in component_form.errors.as_data().items():
                        # Assign errors on the child form's name field to name_pattern on the parent form
                        if field == 'name':
                            field = 'name_pattern'
                    for e in errors:
                        form.add_error(field, '{}: {}'.format(name, ', '.join(e)))

            if not form.errors:
                for modelform in new_components:
                    modelform.save()
                # self.model.objects.bulk_create(new_components)
                if '_addanother' in request.POST:
                    return redirect(request.path)
                else:
                    return redirect(parent.get_detail_url())

        return render(request, self.template_name, {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': parent.get_absolute_url(),
        })






