from ..storage.sqlstorage import Base, GUID, SQLStorage
from .dictprovider import DictProvider
from ..app import App
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from dateutil.parser import parse as _parse_date
import uuid
from ..types import datestr
import pytz
import copy
import datetime
from ...interfaces import ISchema, IDataProvider
from ..util import dataclass_get_type
from dataclasses import _MISSING_TYPE

_MARKER: list = []


def parse_date(datestr):
    d = _parse_date(datestr)
    if d.tzinfo is None:
        d = d.replace(tzinfo=pytz.UTC)
    d = d.astimezone(pytz.UTC)
    return d.replace(tzinfo=None)


class SQLAlchemyModelProvider(IDataProvider):

    def __init__(self, schema, data, storage):
        self.schema = schema
        self.data = data
        self.orm_model = data.__class__
        self.columns = self.orm_model.__table__.c
        self.storage = storage
        self.changed = False

    def __getitem__(self, key):
        if isinstance(self.columns[key].type, sa.DateTime):
            try:
                data = getattr(self.data, key)
            except AttributeError:
                raise KeyError(key)
            if data:
                return data
            return None
        if isinstance(self.columns[key].type, GUID):
            try:
                data = getattr(self.data, key)
            except AttributeError:
                raise KeyError(key)
            if data:
                return data.hex
            return None
        if isinstance(self.columns[key].type, sajson.JSONField):
            try:
                data = getattr(self.data, key)
            except AttributeError:
                raise KeyError(key)
            if data is not None:
                return copy.deepcopy(data)
            return None
        try:
            return getattr(self.data, key)
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if key not in self.columns:
            return
        if value and isinstance(self.columns[key].type, sa.DateTime):
            if not isinstance(value, datetime.datetime):
                value = parse_date(value)
        elif value and isinstance(self.columns[key].type, GUID):
            value = uuid.UUID(value)

        setattr(self.data, key, value)

    def __delitem__(self, key):
        setattr(self.data, key, None)

    def setdefault(self, key, value):
        if self.get(key):
            return
        self.set(key, value)

    def get(self, key, default=_MARKER):
        if default is _MARKER:
            attr = self.schema.__dataclass_fields__.get(key, None)
            if attr:
                #t = dataclass_get_type(attr)
                if attr.default is not _MISSING_TYPE:
                    default = attr.default
                elif attr.default_factory is not _MISSING_TYPE:
                    default = attr.default_factory()
                else:
                    default = None

        if default is not _MARKER:
            try:
                return self[key]
            except KeyError:
                return default
        return self[key]

    def set(self, key, value):
        self[key] = value

    def items(self):
        res = []
        fields = self.schema.__dataclass_fields__.keys()
        for f in fields:
            res.append((f, self.data[f]))
        return res

    def keys(self):
        return self.schema.__dataclass_fields__.keys()

    def as_dict(self):
        fields = self.schema.__dataclass_fields__.items()
        result = {}
        for n, f in fields:
            v = self.get(n)
            t = dataclass_get_type(f)
            if not v and t['metadata']['exclude_if_empty']:
                continue
            result[n] = v
        return result

    def as_json(self):
        fields = self.schema.__dataclass_fields__.items()
        result = {}
        for n, f in fields:
            t = dataclass_get_type(f)
            v = self.get(n)
            if not v and t['metadata']['exclude_if_empty']:
                continue
            if isinstance(v, datetime.datetime):
                result[n] = datestr(v.isoformat())
            else:
                result[n] = v
        return result


@App.dataprovider(schema=ISchema, obj=Base, storage=SQLStorage)
def get_provider(schema, obj, storage):
    return SQLAlchemyModelProvider(schema, obj, storage)


@App.dataprovider(schema=ISchema, obj=dict, storage=SQLStorage)
def get_dict_provider(schema, obj, storage):
    return DictProvider(schema, obj, storage)


@App.jsonprovider(obj=SQLAlchemyModelProvider)
def get_jsonprovider(obj):
    return obj.as_json()
