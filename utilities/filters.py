import django_filters

class NumericInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """filter a set of number filter"""
    pass
