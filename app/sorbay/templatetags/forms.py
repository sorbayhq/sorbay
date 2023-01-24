import itertools
import os

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()
AVAILABLE_FIELDS = list(
    itertools.chain(
        *[
            name.replace(".html", "").split(",")
            for name in os.listdir("/app/templates/forms/fields/")
        ]
    )
)


def raise_for_unknown_fields(fields):
    if unknown_fields := list(set(fields) - set(AVAILABLE_FIELDS)):
        raise ImproperlyConfigured(f"Unrecognized fields {unknown_fields}")


@register.simple_tag(takes_context=True)
def render_form(
    context, form, action="", submit_btn="Senden", field_margin="mb-3", show_label=True
):
    """Custom templatetag zum rendern von Formularen im Design der Dachdigital.

    Beispiele:
    {% load forms %}

    {% render_form form=form %}

    {# form mit angepasstem submit text #}
    {% render_form form=form submit_btn='Speichern' %}

    {# form mit custom action URL #}
    {% with url 'tenders:create' as action #}
        {% render_form form=form action=action %}
    {% endwith %}

    {# form ohne label #}
    {% render_form form=form show_label=False %}
    """
    raise_for_unknown_fields(fields=[field.widget_type for field in form])
    return mark_safe(
        render_to_string(
            "forms/form.html",
            context={
                "form": form,
                "action": action,
                "submit_btn": submit_btn,
                "field_margin": field_margin,
                "show_label": show_label,
            },
            request=context["request"],
        )
    )


@register.simple_tag
def render_field(field, field_margin="mb-3", show_label=True):
    """Custom templatetag zum rendern eines Formular Feldes im Design der Dachdigital.

    Beispiele:
    {% load forms %}

    {% render_field field=form.field %}

    {# field mit margin #}
    {% render_field field=form.field field_margin='mb-5' %}

    {# field ohne Label #}
    {% render_field field=form.field show_label=False %}
    """
    raise_for_unknown_fields((field.widget_type,))
    return mark_safe(
        render_to_string(
            "forms/field.html",
            context={
                "field": field,
                "field_margin": field_margin,
                "show_label": show_label,
            },
        )
    )
