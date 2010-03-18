from Products.Archetypes.interfaces.field import IReferenceField

from z3c.relationfield import interfaces


class IATHasOutgoingRelations(interfaces.IHasOutgoingRelations):
    """An Archetypes object providing outgoing relations."""


class IATHasIncomingRelations(interfaces.IHasIncomingRelations):
    """An Archetypes object providing incoming relations."""


class IATHasRelations(interfaces.IHasRelations,
                      IATHasIncomingRelations,
                      IATHasOutgoingRelations):
    """An Archetypes object providing relations."""
    

class IZCRelationField(IReferenceField):
    """A marker interface for zc relation fields
    """
