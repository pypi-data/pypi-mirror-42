# Copyright (C) 2019 by Dr. Dieter Maurer <dieter@handshake.de>
"""Extensions for Zope2/Zope 4+."""

from zope.interface import implementer

from zope.schema.interfaces import INativeStringLine, ValidationError
from zope.schema import NativeStringLine
from OFS.ObjectManager import bad_id


class IItemName(INativeStringLine):
  """A name (also known as id) for an `OFS.interfaces.IItem`. """

@implementer(IItemName)
class ItemName(NativeStringLine):
  def _validate(self, value):
    super(ItemName, self)._validate(self, value)
    if bad_id(value):
      raise ValidationError(
        # may want internationalization
        self.__name__, "Bad character[s] in ItemName"
        ).with_field_and_value(self, value)


class IItemPath(INativeStringLine):
  """An item path represented as a `"/"` separated sequence of `IItemName`s."""

@implementer(IItemPath)
class ItemPath(NativeStringLine):
  def _validate(self, value):
    super(ItemPath, self)._validate(value)
    if bad_id(value.replace("/", "")):
      raise ValidationError(
        # may want internationalization
        self.__name__, "Bad character[s] in ItemPath"
        ).with_field_and_value(self, value)
      


