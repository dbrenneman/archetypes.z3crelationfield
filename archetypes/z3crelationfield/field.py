from zope.interface import implements
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from AccessControl import ClassSecurityInfo
from zc.relation.interfaces import ICatalog
from z3c.relationfield.relation import RelationValue
from Products.Archetypes.Registry import registerField
from Products.Archetypes.public import ObjectField, ReferenceField
from archetypes.z3crelationfield.interfaces import IZCRelationField


class ZCRelationField(ReferenceField):
    """A field for creating references from Archetypes objects to
    Dexterity objects.
    """
    implements(IZCRelationField)

    def get(self):
        """
        """
        resolved_list = []
        for rel in self.rel_list:
            resolved_list.append(rel.to_object)
        return resolved_list

    def set(self, instance, value, **kwargs):
        """
        """
        if not instance.relations:
            instance.relations = []

        relations_tool = getUtility(ICatalog)
        intid_tool = getUtility(IIntIds)
        instance_id = intid_tool.getId(instance)
        targetIDs = sorted(relations_tool.findRelations({'to_id': instance_id}))
        if value is None:
            value = ()

        if not isinstance(value, (list, tuple)):
            value = value,
        elif not self.multiValued and len(value) > 1:
            raise ValueError, \
                  "Multiple values given for single valued field %r" % self

        #convert objects to intids if necessary
        intids = []
        for v in value:
            if isinstance(v, basestring):
                intids.append(v)
            else:
                intids.append(intid_tool.getID(v))

        add = [v for v in intids if v and v not in targetIDs]
        sub = [t for t in targetIDs if t not in intids]

        for intid in add:
            instance.rel.append(RelationValue(intid))

        for intid in sub:
            pass
            #instance.rel.del('')

        if self.callStorageOnSet:
            #if this option is set the reference fields's values get written
            #to the storage even if the reference field never use the storage
            #e.g. if i want to store the reference UIDs into an SQL field
            ObjectField.set(self, instance, self.getRaw(instance), **kwargs)

        #notify(ObjectModifiedEvent(instance)

registerField(ZCRelationField, title='Relations', description='Used to set relationships between content.')
