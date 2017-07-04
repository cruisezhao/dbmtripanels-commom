from django.utils.html import mark_safe
import django_tables2 as tables

class ToggleColumn(tables.CheckBoxColumn):

    def __init__(self, *args, **kwargs):
        default = kwargs.pop('default', '')
        visible = kwargs.pop('visible', False)
        super(ToggleColumn, self).__init__(*args, default=default, visible=visible, **kwargs)

    @property
    def header(self):
        return mark_safe('<input type="checkbox" id="toggle_all" title="Toggle all" />')
