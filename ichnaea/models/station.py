import colander
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    DOUBLE as Double,
    INTEGER as Integer,
)

from ichnaea.models.base import (
    PositionMixin,
    TimeTrackingMixin,
    ValidPositionSchema,
    ValidTimeTrackingSchema,
)
from ichnaea.models import constants
from ichnaea.models.schema import (
    CopyingSchema,
    FieldSchema,
)


class ValidBaseStationSchema(ValidPositionSchema, ValidTimeTrackingSchema):
    """A schema which validates the fields present in a base station."""

    range = colander.SchemaNode(colander.Integer(), missing=0)
    total_measures = colander.SchemaNode(colander.Integer(), missing=0)


class BaseStationMixin(PositionMixin, TimeTrackingMixin):

    range = Column(Integer)
    total_measures = Column(Integer(unsigned=True))


class ValidBboxSchema(FieldSchema, CopyingSchema):
    """A schema which validates fields present in a bounding box."""

    max_lat = colander.SchemaNode(
        colander.Float(),
        missing=None,
        validator=colander.Range(constants.MIN_LAT, constants.MAX_LAT))
    min_lat = colander.SchemaNode(
        colander.Float(),
        missing=None,
        validator=colander.Range(constants.MIN_LAT, constants.MAX_LAT))

    max_lon = colander.SchemaNode(
        colander.Float(),
        missing=None,
        validator=colander.Range(constants.MIN_LON, constants.MAX_LON))
    min_lon = colander.SchemaNode(
        colander.Float(),
        missing=None,
        validator=colander.Range(constants.MIN_LON, constants.MAX_LON))


class BboxMixin(object):

    max_lat = Column(Double(asdecimal=False))
    min_lat = Column(Double(asdecimal=False))

    max_lon = Column(Double(asdecimal=False))
    min_lon = Column(Double(asdecimal=False))


class ValidStationSchema(ValidBaseStationSchema, ValidBboxSchema):
    """A schema which validates the fields present in a station."""


class StationMixin(BaseStationMixin, BboxMixin):

    new_measures = Column(Integer(unsigned=True))