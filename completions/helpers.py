from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def get_completions(term):
    """Returns a list of dictionaries containing the name suggestions for autocompletion."""
    model = get_model("COMPLETIONS_MODEL")
    field = getattr(settings, "COMPLETIONS_FIELD")
    if not isinstance(field, str):
        raise ImproperlyConfigured(f"{field} must be a string.")
    order = getattr(settings, "COMPLETIONS_ORDER", ['?'])
    if not isinstance(order, list):
        raise ImproperlyConfigured(
            f"{order} must be a list of strings."
        )
    method = getattr(settings, "COMPLETIONS_METHOD", 'icontains')
    if not isinstance(method, str):
        raise ImproperlyConfigured(f"{order} must be a string.")
    kwargs = {f"{field}__{method}": term}
    return list(
        model.objects.filter(**kwargs)
        .order_by(*order)
        .values_list(field, flat=True)[:15]
    )


def get_model(constant_name):
    """Returns the model specified with constant_name in the settings."""
    model_name = getattr(settings, constant_name)
    try:
        return django_apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"{constant_name} must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"{constant_name} refers to model '{model_name}' "
            "that has not been installed"
        )
