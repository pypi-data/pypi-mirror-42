# django-font-icons

A utility for using icons in models and forms.
You can also disable icons so they will no show in the select.

It uses selectr for filtering of the icons.

## Installation / Usage

    pip install django-font-icons

Add 'font_icons' to your installed `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'font_icons',
    )

Import and use `IconForeignKeyField`:

    from font_icons.models import IconForeignKeyField

    class Category(models.Model):
        ...
        icon = IconForeignKeyField()

Add Fontawesome js and/or css yourself. We do not provide a default version.

`admin/base_site.html`
```html
{% block extrastyle %}
    {{ block.super }}
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link href="https://unpkg.com/mobius1-selectr@latest/dist/selectr.min.css" rel="stylesheet" type="text/css">
    <script src="https://unpkg.com/mobius1-selectr@latest/dist/selectr.min.js" type="text/javascript"></script>
{% endblock %}
```


## Rendering

You can do a simple render  in your template like this:

    {% for category in categories.all %}
        {% if category.icon %}
            {{ category.icon.as_html }}
        {% endif %}
    {% endfor %}

## Changes
 - Add the fontawesome 5 Free icons. (`manage.py loadfontawesome5_free`)
 - Support for fontawesome 5 Pro and fontawesome 4.7 (No management command to load all the icons yet.)
