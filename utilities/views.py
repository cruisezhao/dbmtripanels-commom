from django.views.generic import View
from django import forms
from django.db.models import ProtectedError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.formats import mark_safe
from django.utils.html import escape
from django.contrib import messages
from .forms import ComfirmationForm
from .paginator import EnhancedPaginator
from django_tables2 import RequestConfig
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class GetReturnURLMixin(object):
    """where to redirect after process a form"""
    default_return_url = None

    def get_return_url(self, request, obj):
        if self.default_return_url is not None:
            return reverse(self.default_return_url)
        return reverse('home')


class ObjectListView(View):
    """

    List a series of objects

    queryset: The queryset of objects to display
    filter: The django-filter FilterSet that is applied to queryset
    filter_form: The form used to render filter options
    template_name: The name of the template
    """
    queryset = None
    filter = None
    filter_form = None
    template_name = None

    def get(self, request):
        #get method
        model = self.queryset.model
        object_ct = ContentType.objects.get_for_model(model)

        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        self.queryset = self.alter_queryset(request)

        #Construct the table based on the user's permissions
        table = self.table(self.queryset)
        if 'pk' in table.base_columns:
            table.base_columns['pk'].visible = True

        #Apply the request context
        paginate = {
            'klass': EnhancedPaginator,
            'per_page': request.GET.get('per_page', settings.PAGINATE_COUNT)
        }
        RequestConfig(request, paginate).configure(table)
        
        if self.filter_form is None:
            form = self.filter(request.GET, self.queryset).form
        else:
            form = self.filter_form(request.GET, label_suffix='')if self.filter_form else None
            
        context = {
            'table': table,
            'permissions': False,
            'filter_form': form,
            'export_templates': None,
        }
        context.update(self.extra_context())
        return render(request, self.template_name, context)


    def alter_queryset(self, request):
        return self.queryset.all()

    def extra_context(self):
        return {}


class ObjectEditView(GetReturnURLMixin, View):
    """Create or edit a single object."""
    model = None
    form_class = None
    template_name = 'utilities/obj_edit.html'

    def get_object(self, kwargs):
        """look up object by uuid"""
        if hasattr(self.model, 'uuid'):
            return get_object_or_404(self.model, uuid = kwargs['uuid'])
        else:
            return get_object_or_404(self.model, id = kwargs['id'])
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
            #add another
            if '_addanother' in request.POST:
                return redirect(request.path)
            return redirect(self.get_return_url(request, obj))
        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })


class ObjectDeleteView(GetReturnURLMixin, View):
    """
    Delete a single object
    model: The model of object being deleted
    template_name: The name of the template
    default_return_url: Name of the URL to which the user is redirected after deleted the object.
    """
    model = None
    template_name = "utilities/obj_delete.html"

    def get_object(self,kwargs):
        #get a object via uuid
        if hasattr(self.model, 'uuid'):
            return get_object_or_404(self.model, uuid = kwargs['uuid'])
        else:
            return get_object_or_404(self.model, id = kwargs['id'])

    def get(self, request, **kwargs):
        obj = self.get_object(kwargs)
        form = ComfirmationForm(initial = request.GET)

        return render(request, self.template_name, {
            'obj': obj,
            'form': form,
            'obj_type': self.model._meta.verbose_name,
            'return_url': self.get_return_url(request, obj),
        })

    def post(self, request, **kwargs):
        #post delete the obj
        obj = self.get_object(kwargs)
        form = ComfirmationForm(request.POST)
        if form.is_valid():
            try:
                obj.delete()
            except ProtectedError:
                raise ProtectedError(self.model,"the obj can't delete, because the model is protected!")

            msg = "Deleted {} {}".format(self.model._meta.verbose_name, obj)
            messages.success(request, msg)
            return redirect(self.get_return_url(request, obj))
        return render(request, self.template_name, {
            'obj': obj,
            'form': form,
            'obj_type': self.model._meta.verbose_name,
            'return_url': self.get_return_url(request, obj),
        })


class BulkEditView(View):
    """batch change objects"""
    cls = None
    filter = None
    form = None
    template_name = None
    default_return_url = 'home'

    def get(self,request):
        return redirect(self.default_return_url)

    def post(self, request, **kwargs):
        return_url = reverse(self.default_return_url)

        if request.POST.get("_all") and self.filter is not None:
            pk_list = [obj.pk for obj in self.filter(request.GET, self.cls.objects.only('pk')).qs]
        else:
            pk_list = [int(pk) for pk in request.POST.getlist('pk')]

        if '_apply' in request.POST:
            form = self.form(self.cls, request.POST)
            if form.is_valid():
                standard_fields = [field for field in form.fields if field != 'pk']
                # nullified_fields = request.POST.getlist('_nullify')
                fields_to_update = {}
                for field in standard_fields:
                    if form.cleaned_data[field] not in (None, ''):
                        fields_to_update[field] = form.cleaned_data[field]
                updated_count = self.cls.objects.filter(pk__in=pk_list).update(**fields_to_update)

                if updated_count:
                    msg = 'Updated {} {}'.format(updated_count, self.cls._meta.verbose_name_plural)
                    messages.success(self.request, msg)
                return redirect(return_url)

        else:
            initial_data = request.POST.copy()
            initial_data['pk'] = pk_list
            form = self.form(self.cls, initial=initial_data)

        selected_objects = self.cls.objects.filter(pk__in=pk_list)

        if not selected_objects:
            messages.warning(request, "No {} were selected.".format(self.cls._meta.verbose_name_plural))
            return redirect(return_url)
        return render(request, self.template_name, {
            'form': form,
            'selected_objects': selected_objects,
            'return_url': return_url,
        })


class BulkDeleteView(View):
    """bulk delete view"""
    cls = None
    filter = None
    form = None
    template_name = "utilities/confirm_bulk_delete.html"
    default_return_url = 'home'

    def post(self, request, **kwargs):
        return_url = reverse(self.default_return_url)

        if request.POST.get('_all') and self.filter is not None:
            pk_list = [obj.pk for obj in self.filter(request.GET, self.cls.objects.only('pk')).qs]
        else:
            pk_list = [int(pk) for pk in request.POST.getlist('pk')]

        form_cls = self.get_form()
        if '_confirm' in request.POST:
            form = form_cls(request.POST)
            if form.is_valid():

                # Delete objects
                queryset = self.cls.objects.filter(pk__in=pk_list)
                try:
                    deleted_count = queryset.delete()[1][self.cls._meta.label]
                except ProtectedError as e:
                    msg = "Delete objects failed, because of protected error."
                    messages.success(request, msg)
                    return redirect(return_url)

                msg = 'Deleted {} {}'.format(deleted_count, self.cls._meta.verbose_name_plural)
                messages.success(request, msg)
                return redirect(return_url)
        else:
            form = form_cls(initial={'pk': pk_list, 'return_url': return_url})

        selected_objects = self.cls.objects.filter(pk__in=pk_list)
        if not selected_objects:
            messages.warning(request, "No {} were selected for deletion.".format(self.cls._meta.verbose_name_plural))
            return redirect(return_url)

        return render(request, self.template_name, {
            'form': form,
            'obj_type_plural': self.cls._meta.verbose_name_plural,
            'selected_objects': selected_objects,
            'return_url': return_url,
        })

    def get_form(self):

        class BulkDeleteForm(ComfirmationForm):
            pk = forms.ModelMultipleChoiceField(queryset=self.cls.objects.all(), widget=forms.MultipleHiddenInput)

        if self.form:
            return self.form
        return BulkDeleteForm