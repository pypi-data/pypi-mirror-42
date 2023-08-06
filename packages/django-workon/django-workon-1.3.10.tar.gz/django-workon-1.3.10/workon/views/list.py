import datetime
import workon.utils
import workon.conf
from django import forms
from django.db import models
from django.views import generic
from django.shortcuts import render
from django.utils.html import mark_safe
from django.utils import six
from django.utils.text import slugify
from django.forms.fields import CallableChoiceIterator
from django.core.exceptions import FieldDoesNotExist


__all__ = ['ListColumn', 'ListCol', 'ListFilter', 'ListAction', 'List', 'TableList']


    









class ModelListChoiceField(forms.ModelChoiceField):

    empty_label= ''

    pass

class ListChoiceField(forms.ChoiceField):
    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        if callable(value):
            value = CallableChoiceIterator(value)
        else:
            value = list(value)
        self._choices = self.widget.choices = [('', ' -- '), ] + list(value)
    choices = property(_get_choices, _set_choices)


class ListMultipleChoiceField(forms.MultipleChoiceField):
    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        if callable(value):
            value = CallableChoiceIterator(value)
        else:
            value = list(value)
        self._choices = self.widget.choices = list(value)
    choices = property(_get_choices, _set_choices)
















class ListAction():
    def __init__(self, name, label=None, col=2):
        self.name = name
        self.meta = {
            'class': f'col s12 m{col}',
            'label': label or name,
        }










class ListFilter():
    def __init__(self, name, label=None, col=2, choices=None, classes='', 
        multiple=False, default=None, field_class=None, field_kwargs=None,
        linebreaks=False
    ):
        self.name = name
        field_kwargs = field_kwargs if field_kwargs else {}
        field_kwargs['required'] = False
        field_kwargs['initial'] = default
        field_kwargs['label'] = label
        if not field_class:
            if choices is not None:
                if isinstance(choices, models.QuerySet):
                    field_class = ModelListChoiceField
                    field_kwargs['queryset'] = choices
                    field_kwargs['empty_label'] = ''
                else:
                    if multiple == True:
                        field_class = ListMultipleChoiceField
                    else:
                        field_class = ListChoiceField
                    field_kwargs['choices'] = choices
            else:
                field_class = forms.CharField
        self.form_field_kwargs = field_kwargs
        self.form_field_class = field_class
        self.meta = {
            'class': f'{classes}',
            'label': label if label else name,
            'linebreaks': linebreaks
        }



class ListForm(forms.Form):
    def __init__(self, filters_instances,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['page'] = forms.CharField(widget=forms.HiddenInput(), required=False)
        for fi in filters_instances:
            field_kwargs = fi.form_field_kwargs
            self.fields[fi.name] = fi.form_field_class(**field_kwargs)
            self.fields[fi.name].meta = fi.meta
            self.fields[fi.name].filter = fi





class ListColumn():
    def __init__(self, name, label=None, classes='', attrs='', ellipsis=False, col=None, value=None, model=None):
        self.name = name
        self.label = label
        self.classes = classes
        self.attrs = attrs
        self.ellipsis = ellipsis
        self.value = value
        self.model = model

    def __str__(self):
        return str(self.label) if self.label else ''

    @classmethod
    def make_instance(cls, listview, col, **kwargs):
        if isinstance(col, cls):
            col = col

        elif isinstance(col, dict):
            col = cls(**col)

        elif isinstance(col, tuple):
            label = col[-1]
            col = cls.make_instance(listview, col[0], label=col[-1])

        elif isinstance(col, six.string_types):
            col = cls(col, **kwargs)

        if listview.model and not col.label:
            try:
                col.label = listview.model._meta.get_field(col.name).verbose_name
            except FieldDoesNotExist:
                print('FieldDoesNotExist')
                pass
        return col

class ListCol(ListColumn): pass






class List(generic.FormView):

    template_name = workon.conf.LIST_TEMPLATE
    results_template_name = workon.conf.LIST_RESULTS_TEMPLATE
    row_template_name = workon.conf.LIST_ROW_TEMPLATE
    layout_template_name = workon.conf.LIST_LAYOUT_TEMPLATE
    floating_actions_template_name = workon.conf.LIST_FLOATING_ACTIONS_TEMPLATE

    list_id = 'filtered_list'
    list_class = ''
    filters = []
    actions = []
    columns = []
    filters_instances = []
    columns_instances = []
    form_class = None
    form_prefix = 'wlff' # workon_list_filters_form
    model = None
    ajax_results = True

    paginate_by = 50
    paginate_body = 6
    paginate_padding = 2

    create_url = None
    create_method = workon.conf.LIST_ROW_CREATE_METHOD
    update_method = workon.conf.LIST_ROW_UPDATE_METHOD
    view_method = workon.conf.LIST_ROW_VIEW_METHOD
    delete_method = workon.conf.LIST_ROW_DELETE_METHOD
    update_on_double_click_method = workon.conf.LIST_ROW_UPDATE_ON_DOUBLE_CLICK_METHOD

    row_class = ''
    row_style = ''
    row_id = lambda self, obj: f'{obj}_{obj.pk}' if hasattr(obj, 'pk') else str(obj)

    def __get_vomr(self, name):        
        value = getattr(self, f'get_{name}', getattr(self, name, None))
        if workon.utils.is_lambda(value):
            return value()
        elif workon.utils.is_method(value):
            return value()
        else:
            return getattr(self, name, None)

    def __get_vomr_obj(self, name, obj):        
        value = getattr(self, f'get_{name}', getattr(self, name, None))

        ## COMPAT
        if value is None:
            value = getattr(self, f'get_col_{name}', None)
        ## END_COMPAT

        if workon.utils.is_lambda(value):
            return value(obj)
        elif workon.utils.is_method(value):
            return value(obj)
        else:
            return getattr(obj, name, None)

    def __get_vomr_obj_value(self, name, obj):        
        value = getattr(self, f'get_{name}_value', getattr(self, f'{name}_value', None))

        ## COMPAT
        if value is None:
            value = getattr(self, f'get_col_{name}_value', None)
        ## END_COMPAT

        if value is None:
            value = getattr(obj, name, None)

        if workon.utils.is_lambda(value):
            return value(obj)
        elif workon.utils.is_method(value):
            return value(obj)
        else:
            return getattr(obj, name, None)

    def make_filter_instance(self, fi, **kwargs):
        if isinstance(fi, ListFilter):
            fi = fi

        elif isinstance(fi, dict):
            fi = ListFilter(**fi)

        elif isinstance(fi, tuple):
            fi = self.make_filter_instance(fi[0], label=fi[-1])

        elif isinstance(fi, six.string_types):
            name_ftype = fi.split('::', 1)
            ftype = name_ftype[-1]
            name = name_ftype[0]
            if not 'label' in kwargs:
                kwargs['label'] = name
            if len(name_ftype) == 2:
                if ftype == "int":
                    kwargs['field_class'] = forms.IntegerField
                elif ftype in ["bool", "boolean"]:
                    kwargs['field_class'] = forms.BooleanField
                elif ftype in ["hidden"]:
                    kwargs['field_class'] = forms.TextField
                    kwargs['field_kwargs'] = {'widget': forms.HiddenInput()}
                elif ftype in ["date"]:
                    kwargs['field_class'] = workon.forms.DateField
                elif ftype in ["datetime"]:
                    kwargs['field_class'] = workon.forms.DateTimeField
                elif ftype in ["time"]:
                    kwargs['field_class'] = workon.forms.TimeField
            fi = ListFilter(name, **kwargs)
        return fi


    def is_last_object_saved(self, obj):
        return f'{getattr(obj, "__class___", None)}_{getattr(obj, "id", None)}' == self.request.session.get("wls_last_object_saved")

    def get_form(self):

        self.columns_instances = [ ListCol.make_instance(self, col) for col in getattr(self, 'fields', self.columns)]
        self.filters_instances = [ self.make_filter_instance(fi) for fi in self.filters]

        if not self.form_class:
            self.form = ListForm(self.filters_instances, **self.get_form_kwargs())
        else:
            self.form = self.form_class(**self.get_form_kwargs())
        self.form_initialize(self.form)
        return self.form

    def form_initialize(self, form):
        return form

    def get_prefix(self):
        return self.form_prefix
        
    def get_form_kwargs(self):
        prefix = self.get_prefix()
        kwargs = {
            'initial': self.get_initial(),
            'prefix': prefix,
        }
        if self.request.method in ('GET'):
            kwargs.update({
                'initial': {k.lstrip(f'{prefix}-'): v for k,v in self.request.GET.items()},
            })
            if not self.ajax_results:
                kwargs.update({
                    'data': self.request.GET,
                })

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_extra_actions(self, obj):
        return ''

    # def get_row_id(self, obj):
    #     if hasattr(obj, 'pk'):
    #         return f'{obj}_{obj.pk}'
    #     else:
    #         return str(obj)


    # def get_row_attrs(self, obj):
    #     if workon.conf.LIST_ROW_UPDATE_ON_DOUBLE_CLICK:
    #         update_url = self.get_row_update_url(obj)
    #         if update_url:
    #             return f'''\
    #                         {self.get_row_update_on_double_click_method(obj)}="{update_url}" \
    #                         data-tooltip='{{ 
    #                             "content": "Double-clic pour éditer" ,
    #                             "position": "left" 
    #                         }}' '''
    #     return ''

    def get_template_names(self):
        return self.results_template_name if self.request.is_ajax() else self.template_name

    def get_queryset(self):
        qs = []
        if getattr(self, 'model', None):
            qs = self.model.objects.all()
        return self.filter(qs, self.F)

    def filter(self, qs, filters=None):
        if hasattr(self, 'model'):
            pass
        return qs

    def get_rows(self):
        self.rows = []
        self.queryset = getattr(self, 'queryset', [])
        # data = getattr(self.form, 'cleaned_data', { f.name: '' for f in self.filters_instances })
        for obj in self.queryset:
            row = self.get_row(obj)
            self.rows.append(row)
        return self.rows

    def get_row(self, obj):
        cells = []
        for column_instance in self.columns_instances:
            cells.append(self.render_cell(column_instance, obj))
        return {
            'object': obj,
            'id': self.__get_vomr_obj('row_id', obj),
            'attrs': self.__get_vomr_obj('row_attrs', obj),
            'class': self.__get_vomr_obj('row_class', obj),
            'style': self.__get_vomr_obj('row_style', obj),
            'cells': cells,
            'update_method': self.__get_vomr_obj('row_update_method', obj),
            'delete_method': self.__get_vomr_obj('row_delete_method', obj),
            'view_method': self.__get_vomr_obj('row_view_method', obj),
            'extra_actions': self.get_extra_actions(obj),
        }

    @classmethod
    def render_row(cls, request, obj):
        self = cls()
        self.request = request
        self.get_form()
        return workon.render_content(request, self.__get_vomr('row_template_name'), {
            'row': self.get_row(obj)
        })

    def render_cell(self, column_instance, obj):
        data = dict(
            attrs='',
            classes='',
            column=column_instance
        )
        name = column_instance.name 
        if column_instance.value is not None:
            if workon.is_lambda(column_instance.value):
                value = column_instance.value(self, obj)
            elif workon.is_method(column_instance.value):
                value = column_instance.value(self, obj)
            else:
                value = column_instance.value
        else:
            value = self.__get_vomr_obj_value(name, obj)

        if value is None or value is "":
            value = f'''<i class="icon disabled">block</i>'''
        elif isinstance(value, bool):
            value = f'''<i class="icon {'success' if value else 'error'}">{'check' if value else 'close'}</i>'''
        elif isinstance(value, datetime.date):
            value = value.strftime("%d %b <sup>%Y</sup> <sub>à %H:%M</sub>").replace('<sub>à 00:00</sub>', '')
        elif isinstance(value, six.string_types):
            value = value
        data['value'] = value 

        classes = self.__get_vomr_obj(f'{name}_class', obj)#getattr(self, f'get_col_{name}_class', None)
        if classes:
            data['classes'] += classes

        attrs = self.__get_vomr_obj(f'{name}_attrs', obj)
        if attrs:
            data['attrs'] += attrs

        # data['attrs'] = " ".join([f'{name}="{value}"' for name, value in data['attrs'].items()]) 
        return data

    def get_breadbrumbs(self):
        return []

    def form_valid(self, form):
        self.data = self.F = form.cleaned_data
        self.queryset = self.get_queryset()
        action = self.request.GET.get('_action')
        if action and hasattr(self, f'action_{action}'):
            response = getattr(self, f'action_{action}')(self.queryset)
            if not response:
                self.queryset = self.get_queryset()
            elif isinstance(response, models.QuerySet):
                self.queryset = response
            else:
                return response
        return self.render_valid(form)

    def render_valid(self, form):
        # try:
        self.paginate()
        self.rows = self.get_rows()
        # except:
        #     self.queryset = qs
        return render(self.request, self.get_template_names(), self.get_context_data())   

    def paginate(self):
        page_param = f'{self.form_prefix}-page' if self.form_prefix else 'page'
        page = self.data.get(page_param, self.data.get('page'))
        if not page:
            page = self.request.POST.get(page_param, self.request.POST.get('page'))
        if not page:
            page = self.request.GET.get(page_param, self.request.GET.get('page'))
        self.queryset = workon.utils.DiggPaginator(
            self.queryset, 
            self.paginate_by, 
            body=self.paginate_body, 
            padding=self.paginate_padding
        ).get_queryset_for_page(
            page
        )     

    def form_invalid(self, form):
        return self.form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['page_param'] = f'{self.form_prefix}-page' if self.form_prefix else 'page'
        ctx['breadcrumbs'] = self.get_breadbrumbs()
        ctx['columns'] = self.columns_instances
        ctx['actions'] = self.actions
        ctx['rows'] = getattr(self, 'rows', [])
        ctx['objects'] = ctx['queryset'] = getattr(self, 'queryset', [])
        ctx['create_method'] = self.__get_vomr('create_method')
        ctx['create_url'] = self.__get_vomr('create_url')
        ctx['list_results_template'] = self.__get_vomr('results_template_name')
        ctx['list_row_template'] = self.__get_vomr('row_template_name')
        ctx['floating_actions_template'] = self.__get_vomr('floating_actions_template_name')
        ctx['layout_template'] = self.__get_vomr('layout_template_name')
        ctx['list_id'] = self.__get_vomr('list_id')
        ctx['list_class'] = self.__get_vomr('list_class')
        ctx['queryset'] = getattr(self, 'queryset', [])
        return ctx

class RowList(List):
    template_name = "workon/views/list/list.html"
    results_template_name = "workon/views/list/_list.html"
    row_template_name = "workon/views/list/_row.html"
    
    row_nums = 12
    row_tag = 'span'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['row_nums'] = self.row_nums
        ctx['row_tag'] = self.row_tag
        return ctx


class TableList(List):

    template_name = "workon/views/list/list.html"
    results_template_name = "workon/views/list/_list.html"
    row_template_name = "workon/views/list/_row.html"