"""
WTForms Data Source
-------------------

This class will assist in making dynamically generated forms and validation
on your front end. It requires that you have the wtforms library installed.

The main use case is to define your forms and validation in a single class
then use GraphQL to expose the fields in a way that is easy to update. You
will need to define a schema to use this data source, which can either be
generic or you could define a type for each field in the form. Here is an
example schema::

    # expose all attributes you wish to set on input fields these would be
    # values that get set once and not updated
    type FieldAttributes {
        height: String
        max: String
        maxlength: String
        min: String
        placeholder: String
        width: String
    }
    type FieldValidation {
        name: String
        # This is sort of tricky as validation can have tons of different
        # arguments. But you can use the base class to retrieve a
        arguments: String
    }
    type WTFormValidationError {
        fieldName: String
        errors: [String]
    }
    type Field {
        name: String
        label: String
        value: String
        inputType: String
        checked: Boolean
        required: Boolean
        attrs: FieldAttributes
    }
    type GenericForm {
        action: String
        method: String
        fields: [Field]
    }
    extend type Query {
        getNameForm(): GenericForm
    }

Now that you have your schema you can create a form and a datasource for it.
This will connect your form to your schema and allow you to select which
properties you need to display a given form::

    import cannula
    from cannula.datasource.forms import wtforms_resolver
    from wtforms import Form, Length, StringField, DecimalField

    # Register the form, optionally you can pass the name to register
    @wtforms_resolver.register_form()
    class UpdateWidget(Form):
        name = StringField('Widget Name', validators=[Length(max=25)])
        price = DecimalField('Widget Price', validators=[NumberRange(min=4.0)])

    api = cannula.API(__name__)

    # Add the wtforms_resolver to your registered resolvers
    api.register_resolver(wtforms_resolver)

    # Add in your custom resolver to get the form with data
    my_resolver = cannula.resolver(None, schema='''
        extend type Query {
            getUpdateWidgetForm(widgetId: String!) WTForm
        }
    ''')

    @my_resolver.resolve('Query')
    async def getUpdateWidgetForm(source, info, widgetId):
        widget = await info.context.WidgetDatasource.fetch(widgetId)
        # getForm passes all kwargs to the wtform object
        return await info.context.WTForms.getForm('UpdateWidget', obj=widget)

    api.register_resolver(my_resolver)


Now you can serialize this form and send that to your front end for rendering::

    NAME_FORM = parse('''
        getWTForm(name: 'UpdateWidget') {
            action
            method
            fields {
                name
                label
                value
                inputType
                attrs {
                    maxlength
                }
            }
        }
    ''')

    @route('/widget/<widget_id:str>/update')
    def update_widget():
        API.call_sync(NAME_FORM, request=request)
"""

import typing

try:
    import wtforms
except ImportError:
    print('You must install wtforms to use this datasource')

from cannula.api import Resolver


WTFORMS_SCHEMA = """
# WTFORMS_SCHEMA
# --------------
#
# This is the base schema for wtforms, it represents a generic mapping of
# form fields, validators, and errors.
#
# Most attributes are strings, but some such as 'required' are Boolean values
# this union allows us to group all attributes together in single list.
union WTFAttributeValue = String | Boolean

type WTFormsAttributes {
    name: String
    value: WTFormsAttributeValue
}

type WTFormsValidator {
    # The class name of the validator (Length, Required, etc)
    name: String

    # The arguments passed to the validator.
    arguments: [WTFormsAttributes]
}

type WTFormsValidationError {
    fieldName: String
    errors: [String]
}

type WTFormsField {
    name: String!
    inputType: String!
    label: String
    value: String
    attributes: [WTFormsAttributes]
    errors: [String]
}

type WTForm {
    action: String
    method: String
    fields: [WTFormField]
    errors: [String]
}
"""

class WTFormWrapper:

    def __init__(self, form):
        self.form = form

    @property
    def fields(self):



class WTFormDataSource:
    """WTForm Data Source

    This class is a way to use the wtforms library as a datasource.
    """

    # A mapping of requests using the cache_key_for_request. Multiple resolvers
    # could attempt to fetch the same resource, using this we can limit to at
    # most one request per cache key.
    memoized_requests: typing.Dict[str, typing.Awaitable]

    # Resource name for the type that this datasource returns by default this
    # will use the class name of the datasource.
    resource_name: str = 'WTForm'

    def __init__(self, context):
        self.context = context
        self.memoized_requests = {}
        self._forms = {}
        self.assert_has_resource_name()

    def assert_has_resource_name(self) -> None:
        if self.resource_name is None:
            self.resource_name = self.__class__.__name__

    @property
    def __typename(self):
        return self.resource_name

    def get_form(self, form_name: str):
        return self._forms.get(form_name)

    def register_form(self):
        def decorator(klass):
            self._forms[klass.__name__] = klass
        return decorator


wtforms_resolver = Resolver(schema=WTFORMS_SCHEMA)
