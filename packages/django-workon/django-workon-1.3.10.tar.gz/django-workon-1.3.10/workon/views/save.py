import uuid
from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from django.forms import models as model_forms
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import workon.utils
import workon.conf


__all__ = ['Save', 'ModalSave', 'JsonSave', 'SaveField']


class SaveField():
    def __init__(self, name, label=None, required=False, col=12):
        self.name = name
        self.label = label
        self.required = required
        self.meta = {
            'class': f'col s12 m{col}',
            'label': label or name,
        }


def form_save_instance(self, commit=True, **kwargs):
    """
    Save this form's self.instance object if commit=True. Otherwise, add
    a save_m2m() method to the form which can be called after the instance
    is saved manually at a later time. Return the model instance.
    """
    if self.errors:
        raise ValueError(
            "The %s could not be %s because the data didn't validate." % (
                self.instance._meta.object_name,
                'created' if self.instance._state.adding else 'changed',
            )
        )
    if commit:
        # If committing, save the instance and the m2m data immediately.
        self.instance.save( **kwargs)
        self._save_m2m()
    else:
        # If not committing, add a method to the form to allow deferred
        # saving of m2m data.
        self.save_m2m = self._save_m2m
    return self.instance

class Save(generic.UpdateView):

    layout_template_name = workon.conf.SAVE_LAYOUT_TEMPLATE
    template_name = workon.conf.SAVE_TEMPLATE
    result_template_name = "workon/views/list/_row.html"
    modal_actions_template_name = workon.conf.SAVE_MODAL_ACTIONS_TEMPLATE
    fields = None
    form_class = None
    form_classes = ''
    modal_classes = ''
    model = None

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    
    def get_template_names(self):
        if self.request.is_ajax():
            return getattr(self, 'ajax_template_name', 
                        getattr(self, 'template_name_ajax', 
                            getattr(self, 'xhr_template_name', 
                                getattr(self, 'template_name_xhr', 
                                    getattr(self, 'template_name')
                                )
                            )

                        )
                    )
        else:
            return self.template_name

    def get_form_id(self):
        return uuid.uuid1()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if self.model is None:
            kwargs.pop('instance', None)
        else:         
            instance = getattr(self, 'object', None)   
            if instance:
                kwargs.update({'instance': instance})
        return kwargs

    def get_form_class(self):

        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured("Specifying both 'fields' and 'form_class' is not permitted.")
        if self.form_class:
            return self.form_class
        else:
            model = None
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                model = self.object.__class__
            else:
                qs = self.get_queryset()
                if qs is not None:
                    model = qs.model

            if model:

                if self.fields is None:
                    raise ImproperlyConfigured("Using ModelFormMixin (base class of %s) without the 'fields' attribute is prohibited." % self.__class__.__name__)

                fields = []
                for i, field in enumerate(self.fields):
                    if isinstance(field, SaveField):
                        fields.append(field.name)
                    elif isinstance(field, dict):
                        self.fields[i] = field = SaveField(**field)
                        fields.append(field.name)
                    else:
                        fields.append(field)
                form_class = model_forms.modelform_factory(model, fields=fields)
                form_class.save = form_save_instance

            else:
                form_class = self.form_class
            return form_class

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                return None
        return self.queryset.all()


    def form_initialize(self, form):
        return form

    def get_form(self, *args, **kwargs):


        self.form = super().get_form(*args, **kwargs)
        self.form_id = self.get_form_id()
        for name, field in self.form.fields.items():
            if hasattr(self, f'get_field_{name}'):
                self.form.fields[name] = getattr(self, f'get_field_{name}')()
           
        self.form_initialize(self.form)
        for field in self.form.fields.values():
            field.meta = {
                'class': f'col s12',
                'label': field.label,
            }
        if self.fields:
            for field in self.fields:
                if isinstance(field, SaveField):
                    if self.form.fields.get(field.name):
                        self.form.fields[field.name].label = (field.label or self.form.fields[field.name].label).capitalize()
                        self.form.fields[field.name].meta.update(field.meta)

        return self.form

    @property
    def save_and_continue(self):
        return bool(self.request.POST.get('_save_and_continue'))

    def get_object(self, *args, **kwargs):
        if hasattr(self, '_object'):
            return getattr(self, '_object')
        self.created = False
        try:
            self.object = super().get_object()
        except AttributeError:
            self.object = self.model() if self.model else None
            self.created = True

        setattr(self, '_object', self.object)
        return self.object

    def get_save_url(self):
        return self.request.get_full_path()

    def render_form(self, **kwargs):
        return workon.render_content(self.request, self.get_template_names(), self.get_context_data(**{
            'form': self.form
        }, **kwargs))

    def render_row(self, obj):
        return workon.render_content(self.request, self.result_template_name, {
            'row': {
                'object': obj,
                'id': f'{obj}_{obj.pk}'
            }
        })

    
    def get_success_message_json_notice(self):
        return {
            'content': self.get_success_message(self.object),
            'classes': 'success'
        }

    def get_success_message(self, obj):
        return f'{obj} enregistré'

    def form_valid(self, *args, **kwargs):
        self.object = obj = self.save()
        success_message = self.get_success_message(obj)
        messages.success(self.request, success_message)
        return HttpResponseRedirect(self.get_success_url())

    def save(self, *args, **kwargs):
        self.request.session['wls_last_object_saved'] = f'{getattr(self.object, "__class___", None)}_{getattr(self.object, "id", None)}'
        return self.form.save()

    def render_modal_title(self):
        return str(self.object)

    def render_script(self):
        return ""

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['save_url'] = self.get_save_url()
        ctx['form_classes'] = self.form_classes
        ctx['modal_classes'] = self.modal_classes
        ctx['extra_script'] = self.render_script() 
        ctx['layout_template'] = self.layout_template_name
        ctx['modal_actions_template_name'] = self.modal_actions_template_name
        ctx['form_id'] = self.form_id
        ctx['title'] = self.render_modal_title()
        return ctx


class JsonSave(Save):

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_success_continue_url(self):
        return None

    def get_valid_json(self, obj, **kwargs):
        success_message = self.get_success_message(obj)
        kwargs['save_url'] = getattr(obj, 'update_url', self.get_save_url)()
        json = {
            'formAction': kwargs['save_url'],
            'notice': {
                'content': success_message,
                'classes': 'success'
            }
        }
        if self.save_and_continue:
            self.form = self.get_form()
            self.form.instance = obj
            success_continue_url = self.get_success_continue_url()
            if success_continue_url:
                messages.success(self.request, success_message)
                json['redirect'] = success_continue_url
            else:
                json['replace'] = self.render_form(**kwargs)
        else:
            messages.success(self.request, success_message)
            json['redirect'] = self.get_success_url()

        json.update(kwargs)
        return json

    def render_valid(self, obj, **kwargs):
        return JsonResponse(self.get_valid_json(obj, **kwargs))

    def form_valid(self, *args, **kwargs):
        obj = self.save()
        return self.render_valid(obj)

class ModalSave(JsonSave):
    template_name = "workon/views/save/_modal.html"
    
    def get_json_data(self, obj, **kwargs):
        success_message = self.get_success_message(obj)
        kwargs['save_url'] = getattr(obj, 'update_url', self.get_save_url)()
        json = {
            'formAction': kwargs['save_url'],
            'notice': {
                'content': success_message,
                'classes': 'success'
            }
        }
        if self.save_and_continue:
            self.form = self.get_form()
            self.form.instance = obj
            json['replaceModal'] = self.render_form(**kwargs)
        else:
            messages.success(self.request, success_message)
            json['redirect'] = self.request.META['HTTP_REFERER']

        json.update(kwargs)
        return json

    def render_valid(self, obj, **kwargs):
        return JsonResponse(self.get_json_data(obj, **kwargs))

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['is_modal'] = True
        return ctx