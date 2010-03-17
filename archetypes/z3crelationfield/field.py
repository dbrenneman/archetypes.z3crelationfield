from zope.interface import implements
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from AccessControl import ClassSecurityInfo
from z3c.relationfield.relation import RelationValue
from Products.Archetypes.Registry import registerField
from Products.Archetypes.public import ReferenceField
from archetypes.z3crelationfield.interfaces import IZCRelationField


class ZCRelationField(ReferenceField):
    """A field for creating references from Archetypes objects to
    Dexterity objects.
    """
    implements(IZCRelationField)

    rel_list = []
    security  = ClassSecurityInfo()

    security.declarePrivate('get')

    def get(self):
        """
        """
        resolved_list = []
        for rel in self.rel_list:
            if rel.isBroken():
                continue  # FIXME
            resolved_list.append(rel.to_object)
        return resolved_list

    security.declarePrivate('set')

    def set(self, value=[]):
        """
        """
        new_relationships = []
        intids = getUtility(IIntIds)
        to_id = intids.getId(value)
        for item in value:
            to_id = intids.getId(item)
            new_relationships.append(RelationValue(to_id))
        if new_relationships:
            self.rel_list = new_relationships


registerField(ZCRelationField, title='Relations', description='Used to set relationships between content.')
