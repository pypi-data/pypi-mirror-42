# django-formed

A form designer which can create multi-page forms with fieldsets, rows and multiple fields per row. Also an optional
summary page, multiple notification recipients, an automatic confirmation E-mail and custom form fields are possible.

The forms are built using pure Django forms which handle all validation and cleaning of form fields. The lay-out of the
forms is handled in overridable templates. Developers can choose to render the form, fieldset, row or field
automatically by simply printing them or manually by iterating them and printing every bit of HTML themselves.

## Table of contents

- [Installation](#markdown-header-installation)
    + [Dependencies](#markdown-header-dependencies)
    + [Compatibility](#markdown-header-compatibility)
- [Configuration](#markdown-header-configuration)
- [Adding custom form fields](#markdown-header-adding-custom-form-fields)
- [Credits](#markdown-header-credits)

## Installation

Installing Formed is done via PyPi.

    pip install django-formed

After installation the required database tables are creating by running the migration scripts.

    python manage.py migrate

### Dependencies

Formed has the following dependencies:

- [Django](https://www.djangoproject.com/) *duh..*, at least version 1.6.11 and &lt;= 1.9
- [jsonfield](https://github.com/bradjasper/django-jsonfield) 1.0.3

### Compatibility

Formed supports Python 2.7 to 3.5.

## Configuration

Formed does not need any specific configuration but allows developers to customize a lot.
Here are all useful settings:

- `FORMED_FORM_FIELD_MODULES`, default: `(formed.form_fields, django.forms)`. Define which modules should be checked for
   form fields.
- `FORMED_SESSION_NAME`, default: `'formed'`. The name of the session key in which the form data is stored.
- `FORMED_DEFINITION_DEFAULT_FIELD_TYPE`, default: `'CharField'`.

### Notifications

- `FORMED_NOTIFICATION_FROM_EMAIL`, default: `settings.DEFAULT_FROM_EMAIL`. The E-mail from which notifications are
   sent.
- `FORMED_NOTIFICATION_DEFAULT_SUBJECT`, default: `"Submission of form '{name}'"`. The subject of notification E-mails.
   Available tokens are: `{name}`: The name of the form, `{language}` the current language and `{site}` the current
   `Site` object (only when `FORMED_USE_SITES_FRAMEWORK` == `True`).

### Form field rendering

- `FORMED_FORM_ERROR_CSS_CLASS`, default: `'is-error'`. Passed to Django's Form class as the
   [`error_css_class`](https://docs.djangoproject.com/en/1.9/ref/forms/api/#django.forms.Form.error_css_class)
   parameter.
- `FORMED_FORM_REQUIRED_CSS_CLASS`, default: `'is-required'`. Passed to Django's Form class as the
   [`required_css_class`](https://docs.djangoproject.com/en/1.9/ref/forms/api/#django.forms.Form.required_css_class)
   parameter.
- `FORMED_FORM_OPTIONAL_CSS_CLASS`, default: `'is-optional'`. Not a real Django Form class parameter but this class is
   added to the form field container when the field is optional. The reason this setting exists is due to the fact that
   in practice, most fields are required. Not optional.
- `FORMED_FORM_LABEL_SUFFIX`, default `''`. Passed to Django's Form class as the
   [`label_suffix`](https://docs.djangoproject.com/en/1.9/ref/forms/api/#django.forms.Form.label_suffix) parameter.
- `FORMED_FORM_REQUIRED_LABEL_SUFFIX`, default: `None`. The suffix added to a label when a field is required.
- `FORMED_FORM_OPTIONAL_LABEL_SUFFIX`, default: `_(' (optional)')`. The suffix added when a field is optional.

### Admin

- `FORMED_SHOW_JSON_FIELD`, default: `settings.DEBUG`. Boolean value whether or not to show the JSON field in the admin.
- `FORMED_ADDITIONAL_FORM_FIELDS`, default: `{}`. A dictionary of additional form field types. Use this to add more form
   fields. See [Adding custom form fields](#custom-form-fields).
- `FORMED_FORM_FIELDS`, default: `formed.settings.defaults.FORMED_FORM_FIELDS`. A dictionary with field type names as keys
   and dictionaries with field properties as values. This setting overrides **all** available form fields. See
   [Adding custom form fields](#custom-form-fields).
- `FORMED_FORM_FIELD_CATEGORIES`, default: `formed.settings.defaults.FORMED_FORM_FIELD_CATEGORIES`. A dictionary
   with keys as category names and lists with field types. Override or extend this setting to add your own custom
   fields. See [Adding custom form fields](#custom-form-fields).


### reCAPTCHA
- `FORMED_USE_RECAPCHA`, default: `False`. Boolean value whether or not to use the reCAPTCHA option
- `RECAPTCHA_SITE_KEY`, default: `None`. The reCAPTCHA site key as supplied by google
- `RECAPTCHA_SECRET_KEY`, default: `None`. The reCAPTCHA secret key as supplied by google
- `RECAPTCHA_SITE_VERIFY`, default: `https://www.google.com/recaptcha/api/siteverify`. 



### Third party integrations

- `FORMED_USE_SITES_FRAMEWORK`, default: `'django.contrib.sites' in settings.INSTALLED_APPS`. Whether or not to add a
   sites form field to the FormDefinition Model.

## Adding custom form fields

**Step 1**. To add a custom form field you first need a custom field. Simply create a new file in your project, for example
`form_fields.py` and create your form field. You could for example subclass one of the existing fields and add your own
widget.

```
#!python

from django import forms

class MyCustomCharField(forms.CharField):
    widget = MyCustomWidget
```
For more information on how to create form fields please see the
[Django documentation](https://docs.djangoproject.com/en/1.9/ref/forms/fields/#creating-custom-fields).

**Step 2**. In your settings add your form fields module to the `FORMED_FORM_FIELD_MODULES`. This allows Formed to
actually find your custom fields.
```
#!python
from my_project import form_fields

FORMED_ADDITIONAL_FORM_FIELD_MODULES = [form_fields]
```
**Step 3**. In your settings use the setting `FORMED_ADDITIONAL_FORM_FIELDS` to make sure the editor knows how to
handle your form field.
```
#!python
FORMED_ADDITIONAL_FORM_FIELDS = {
    'custom_text': {
        # The type is the class name of our field.
        'type': 'MyCustomCharField',
        # The name of the field in the drop down in the form editor.
        'name': _('Custom text'),
        # The 'component' is used in the form editor in the admin.
        'component': {
            # The name of the component template:
            'name': 'text-input',
            # Additional parameters are passed in the component:
            'type': 'text',
        }
    },
}
```

**Step 4**. Add your field in the `FORMED_FORM_FIELD_CATEGORIES` dictionary. This actually adds your field in the field
types drop down.

```
#!python
from formed.settings.defaults import FORMED_FORM_FIELD_CATEGORIES
from django.utils.translation import ugettext as _

FORMED_FORM_FIELD_CATEGORIES.update({
    # We use gettext to make this category translatable, this is not required.
    _('My custom fields'): [
        # This is the key of our field in the FORMED_ADDITIONAL_FORM_FIELDS variable:
        'custom_text',
    ]
})
```

Your new field is now available in the editor and will be rendered in the template.

## Credits

The admin interface uses the following JS libraries:

- [Vue](https://vuejs.org/) for the editor.
- [Sortable](https://github.com/RubaXa/Sortable) for drag and drop interaction.
