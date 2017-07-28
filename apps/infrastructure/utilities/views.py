from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View


class ComponentCreateView(View):
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
            data = form.cleaned_data

            for name in form.cleaned_data['name_pattern']:
                component_data = {
                    self.parent_field: parent.pk,
                    'name': name,
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
                self.model.objects.bulk_create(new_components)
                messages.success(request, "Added {} {} to {}.".format(
                    len(new_components), self.model._meta.verbose_name_plural, parent
                ))
                if '_addanother' in request.POST:
                    return redirect(request.path)
                else:
                    return redirect(parent.get_absolute_url())

        return render(request, self.template_name, {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': parent.get_absolute_url(),
        })