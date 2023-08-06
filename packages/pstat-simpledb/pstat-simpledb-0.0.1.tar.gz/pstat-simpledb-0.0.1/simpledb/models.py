import simpledb
import datetime
import uuid
import config

__all__ = ['ItemName', 'FieldError', 'Field', 'NumberField', 'BooleanField', 'DateTimeField', 'Manager', 'Model']


class FieldError(Exception): pass


class Field(object):
    name = False

    def __init__(self, default=None, required=False, islist=False):
        self.default = default
        self.required = required
        self.islist = islist

    def install(self, name, cls):
        default = self.default
        # If the default argument is a callable, call it.
        if callable(default):
            default = default()
        setattr(cls, name, default)

    def decode(self, value):
        """Decodes an object from the datastore into a python object."""
        if self.islist and not isinstance(value, (list, tuple)):
            return [value]
        return value

    def encode(self, value):
        """Encodes a python object into a value suitable for the backend datastore."""
        return value


class ItemName(Field):
    """The item's name. Must be a UTF8 string."""
    name = True


class NumberField(Field):
    def __init__(self, padding=0, offset=0, precision=0, **kwargs):
        self.padding = padding
        self.offset = offset
        self.precision = precision
        super(NumberField, self).__init__(**kwargs)

    def encode(self, value):
        """
        Converts a python number into a padded string that is suitable for storage
        in Amazon SimpleDB and can be sorted lexicographically.

        Numbers are shifted by an offset so that negative numbers sort correctly. Once
        shifted, they are converted to zero padded strings.
        """
        padding = self.padding
        if self.precision > 0 and self.padding > 0:
            # Padding shouldn't include decimal digits or the decimal point.
            padding += self.precision + 1
        return super(NumberField, self).encode(('%%0%d.%df' % (padding, self.precision)) % (value + self.offset))

    def decode(self, value):
        """
        Decoding converts a string into a numerical type then shifts it by the
        offset.
        """
        return super(NumberField, self).decode(float(value) - self.offset)


class BooleanField(Field):
    def encode(self, value):
        """
        Converts a python boolean into a string '1'/'0' for storage in SimpleDB.
        """
        return super(BooleanField, self).encode(('0','1')[value])

    def decode(self, value):
        """
        Converts an encoded string '1'/'0' into a python boolean object.
        """
        return super(BooleanField, self).decode({'0': False, '1': True}[value])


class DateTimeField(Field):
    def __init__(self, format='%Y-%m-%dT%H:%M:%S', **kwargs):
        self.format = format
        super(DateTimeField, self).__init__(**kwargs)

    def encode(self, value):
        """
        Converts a python datetime object to a string format controlled by the
        `format` attribute. The default format is ISO 8601, which supports
        lexicographical order comparisons.
        """
        return super(DateTimeField, self).encode(value.strftime(self.format))

    def decode(self, value):
        """
        Decodes a string representation of a date and time into a python
        datetime object.
        """
        return super(DateTimeField, self).decode(datetime.datetime.strptime(value, self.format))


class FieldEncoder(simpledb.AttributeEncoder):
    def __init__(self, fields):
        self.fields = fields

    def encode(self, domain, attribute, value):
        try:
            field = self.fields[attribute]
        except KeyError:
            return value
        else:
            return field.encode(value)

    def decode(self, domain, attribute, value):
        try:
            field = self.fields[attribute]
        except KeyError:
            return value
        else:
            return field.decode(value)


class Query(simpledb.Query):
    def values(self, *fields):
        # If you ask for specific values return a simpledb.Item instead of the Model
        q = self._clone(klass=simpledb.Query)
        q.fields = fields
        return q

    def _get_results(self):
        if self._result_cache is None:
            # If there's a NextToken, we need to keep iterating
            results = []
            response = self.domain.select(self.to_expression())
            items = response['items']
            next_token = response['next_token']
            while True:
                results.extend([self.domain.model.from_item(item) for item in items])

                if next_token is None:
                    break
                response = self.domain.select(
                    self.to_expression(),
                    next_token=next_token.text,
                )
                items = response['items']
                next_token = response['next_token']

            self._result_cache = results

        return self._result_cache


class Manager(object):
    # Tracks each time a Manager instance is created. Used to retain order.
    creation_counter = 0

    def __init__(self):
        self._set_creation_counter()
        self.model = None

    def install(self, name, model):
        self.model = model
        setattr(model, name, ManagerDescriptor(self))
        if not getattr(model, '_default_manager', None) or self.creation_counter < model._default_manager.creation_counter:
            model._default_manager = self

    def _set_creation_counter(self):
        """
        Sets the creation counter value for this instance and increments the
        class-level copy.
        """
        self.creation_counter = Manager.creation_counter
        Manager.creation_counter += 1

    def filter(self, *args, **kwargs):
        return self._get_query().filter(*args, **kwargs)

    def all(self):
        return self._get_query()

    def count(self):
        return self._get_query().count()

    def values(self, *args):
        return self._get_query().values(*args)

    def item_names(self):
        return self._get_query().item_names()

    def get(self, name):
        return self.model.from_item(self.model.Meta.domain.get(name))

    def get_items(self, names):
        if not isinstance(names, (list, str)):
            raise TypeError("parameter 'names' must of type either string or list of strings")
        if not isinstance(names, list) and isinstance(names, str):
            names = [names]
        return [self.model.from_item(\
                self.model.Meta.domain.get(name))
                for name in names]

    def set_limit(self, limit):
        return self._get_query().set_limit(limit)

    def select(self, query, next_token = None):
        set_next_token = lambda x: x.text if x!=None else x
        result = self.model.Meta.domain.select(query, next_token)
        return {'items': [self.model.from_item(item) for item in
                          result['items']],
                'next_token': set_next_token(result['next_token'])
                }

    def _get_query(self):
        return Query(self.model.Meta.domain)


class ManagerDescriptor(object):
    # This class ensures managers aren't accessible via model instances.
    # For example, Poll.objects works, but poll_obj.objects raises AttributeError.
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, type=None):
        if instance != None:
            raise AttributeError("Manager isn't accessible via %s instances" % type.__name__)
        return self.manager


class ModelMetaclass(type):
    """
    Metaclass for `simpledb.models.Model` instances. Installs
    `simpledb.models.Field` instances declared as attributes of the
    new class.
    """

    def __new__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, ModelMetaclass)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)
        fields = {}

        for base in bases:
            if isinstance(base, ModelMetaclass) and hasattr(base, 'fields'):
                fields.update(base.fields)

        new_fields = {}
        managers = {}

        # Move all the class's attributes that are Fields to the fields set.
        for attrname, field in attrs.items():
            if isinstance(field, Field):
                new_fields[attrname] = field
                if field.name:
                    # Add _name_field attr so we know what the key is
                    if '_name_field' in attrs:
                        raise FieldError("Multiple key fields defined for model '%s'" % name)
                    attrs['_name_field'] = attrname
            elif attrname in fields:
                # Throw out any parent fields that the subclass defined as
                # something other than a field
                del fields[attrname]

            # Track managers
            if isinstance(field, Manager):
                managers[attrname] = field

        fields.update(new_fields)
        attrs['fields'] = fields
        new_cls = super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

        for field, value in new_fields.items():
            new_cls.add_to_class(field, value)

        if not managers:
            managers['objects'] = Manager()

        for field, value in managers.items():
            new_cls.add_to_class(field, value)

        if hasattr(new_cls, 'Meta'):
            # If the new class's Meta.domain attribute is a string turn it into
            # a simpledb.Domain instance.
            if isinstance(new_cls.Meta.domain, basestring):
                new_cls.Meta.domain = simpledb.Domain(new_cls.Meta.domain, new_cls.Meta.connection)
            # Install a reference to the new model class on the Meta.domain so
            # Query can use it.
            # TODO: Should we be using weakref here? Not sure it matters since it's
            # a class (global) that's long lived anyways.
            new_cls.Meta.domain.model = new_cls

            # Set the connection object's AttributeEncoder
            new_cls.Meta.connection.encoder = FieldEncoder(fields)

        return new_cls

    def add_to_class(cls, name, value):
        if hasattr(value, 'install'):
            value.install(name, cls)
        else:
            setattr(cls, name, value)


class Model(object):

    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        if config.AUTO_GENERATE_MISSING_KEY and \
                not kwargs.get(self._name_field):
            setattr(self, self._name_field, uuid.uuid4())
        for name, value in kwargs.items():
            setattr(self, name, value)
        self._item = None

    def _get_name(self):
        return getattr(self, self._name_field)

    def save(self):
        if self._item is None:
            self._item = simpledb.Item(self.Meta.connection, self.Meta.domain, self._get_name())
        for name, field in self.fields.items():
            if field.name:
                continue
            value = getattr(self, name)
            if value is None:
                if field.required:
                    raise FieldError("Missing required field '%s'" % name)
                else:
                    del self._item[name]
                    continue
            self._item[name] = value
        self._item.save()

    def delete(self):
        del self.Meta.domain[self._get_name()]

    @classmethod
    def from_item(cls, item):
        obj = cls()
        obj._item = item
        for name, field in obj.fields.items():
            if name in obj._item:
                ##fix for the case when there is only one value in a multivalued attribute.
                ##psdb.simpledb._parse_attributes does not and cannot (since it does not know about models)
                ##takes care of this.
                ##but this requires a default to be specified in the field declaration
                if isinstance(obj.__getattribute__(name), list) and isinstance(obj._item[name], str):
                    obj._item[name] = [obj._item[name]]
                ##
                setattr(obj, name, obj._item[name])
        setattr(obj, obj._name_field, obj._item.name)
        return obj
