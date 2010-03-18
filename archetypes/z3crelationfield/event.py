import grokcore.component as grok

from zope import component
from zope.event import notify
from zope.app.intid.interfaces import (IIntIds,
                                       IIntIdRemovedEvent,
                                       IIntIdAddedEvent)
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent

from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import (IHasOutgoingRelations,
                                          IHasIncomingRelations,
                                          IRelation, IRelationList,
                                          IRelationValue,
                                          ITemporaryRelationValue)

from archetypes.z3crelationfield.interfaces import IZCRelationField


def addRelations(obj, event):
    """Register relations.

    Any relation object on the object will be added.
    """
    for name, relation in _relations(obj):
        _setRelation(obj, name, relation)


# zope.app.intid dispatches a normal event, so we need to check that
# the object has relations.  This adds a little overhead to every
# intid registration, which would not be needed if an object event
# were dispatched in zope.app.intid.
@grok.subscribe(IIntIdAddedEvent)
def addRelationsEventOnly(event):
    obj = event.object
    if not IHasOutgoingRelations.providedBy(obj):
        return
    addRelations(obj, event)


@grok.subscribe(IHasOutgoingRelations, IObjectRemovedEvent)
def removeRelations(obj, event):
    """Remove relations.

    Any relation object on the object will be removed from the catalog.
    """
    catalog = component.queryUtility(ICatalog)
    if catalog is None:
        return

    for name, relation in _relations(obj):
        if relation is not None:
            try:
                catalog.unindex(relation)
            except KeyError:
                # The relation value has already been unindexed.
                pass

@grok.subscribe(IHasOutgoingRelations, IObjectModifiedEvent)
def updateRelations(obj, event):
    """Re-register relations, after they have been changed.
    """
    catalog = component.queryUtility(ICatalog)
    intids = component.queryUtility(IIntIds)

    if catalog is None or intids is None:
        return

    # check that the object has an intid, otherwise there's nothing to be done
    try:
        obj_id = intids.getId(obj)
    except KeyError:
        # The object has not been added to the ZODB yet
        return

    # remove previous relations coming from id (now have been overwritten)
    # have to activate query here with list() before unindexing them so we don't
    # get errors involving buckets changing size
    rels = list(catalog.findRelations({'from_id': obj_id}))
    for rel in rels:
        catalog.unindex(rel)

    # add new relations
    addRelations(obj, event)


def _setRelation(obj, name, value):
    """Set a relation on an object.

    Sets up various essential attributes on the relation.
    """
    # if the Relation is None, we're done
    if value is None:
        return
    # make sure relation has a __parent__ so we can make an intid for it
    value.__parent__ = obj
    # also set from_object to parent object
    value.from_object = obj
    # and the attribute to the attribute name
    value.from_attribute = name
    # now we can create an intid for the relation
    intids = component.getUtility(IIntIds)
    id = intids.register(value)
    # and index the relation with the catalog
    catalog = component.getUtility(ICatalog)
    catalog.index_doc(id, value)


def _relations(obj):
    """Given an object, return tuples of name, relation value.

    Only real relations are returned, not temporary relations.
    """
    for name, index, relation in _potential_relations(obj):
        if IRelationValue.providedBy(relation):
            yield name, relation


def _potential_relations(obj):
    """Given an object return tuples of name, index, relation value.

    Returns both IRelationValue attributes as well as ITemporaryRelationValue
    attributes.

    If this is a IRelationList attribute, index will contain the index
    in the list. If it's a IRelation attribute, index will be None.
    """
    import pdb; pdb.set_trace() # FIXME
    for field in obj.Schema().fields():
        if not IZCRelationField.providedBy(obj):
            continue

        name = field.getName()
        value = field.getAccessor(obj)()

        if not (isinstance(value, (list, tuple))
                or IRelationValue.providedBy(value)):
            continue

        if not field.multiValued:
            yield name, None, value

        else:
            for i, relation in enumerate(value):
                yield name, i, relation
