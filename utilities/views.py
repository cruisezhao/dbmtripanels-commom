from django.views.generic import View
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.formats import mark_safe
from django.utils.html import escape
from django.contrib import messages


class GetReturnURLMixin(object):
    """where to redirect after process a form"""
    default_return_url = None

    def get_return_url(self, request, obj):
        if self.default_return_url is not None:
            return reverse(self.default_return_url)
        return reverse('home')


class ObjectEditView(GetReturnURLMixin, View):
    """Create or edit a single object."""
    model = None
    form_class = None
    template_name = 'utilities/obj_edit.html'

    def get_object(self, kwargs):
        """look up object by uuid"""
        if 'uuid' in kwargs:
            return get_object_or_404(self.model, uuid = kwargs['uuid'])
        return self.model()

    def get(self, request, *args, **kwargs):
        obj = self.get_object(kwargs)
        initial_data = {k: request.GET[k] for k in request.GET}
        form = self.form_class(instance=obj, initial=initial_data)

        return render(request, self.template_name,{
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        form = self.form_class(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            object_created = not form.instance.pk
            obj = form.save()

            msg = 'Created' if object_created else 'Modified'
            msg += self.model._meta.verbose_name
            if hasattr(obj, 'get_absolute_url'):
                msg = '{} <a href="{}">{}</a>'.format(msg, obj.get_absolute_url, escape(obj))
            else:
                msg = '{} {}'.format(msg, escape(obj))
            messages.success(request, mark_safe(msg))
            return redirect(self.get_return_url(request, obj))
        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })