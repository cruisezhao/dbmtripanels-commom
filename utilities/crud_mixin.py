'''
Created on May 18, 2017

@author: ben
'''
class CrudContextMixin(object):
    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """context for render"""
        #initial_data = dict(zip(cls.search_fields,[request.GET.get(field,None) for field in cls.search_fields]))
        context['search_fields'] = cls.search_fields
        return context
    
class CrudQuerySetMixin(object):
    @classmethod
    def custom_queryset(cls, request, **kwargs):
        """custom queryset"""
        kwargs = {}
        for search_key in cls.search_fields:
            if search_key in request.GET and request.GET[search_key]:
                kwargs[search_key] = request.GET[search_key]
        res = cls.model.objects.filter(**kwargs)
        return res
