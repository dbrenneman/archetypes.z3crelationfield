from zope.interface import implements
from zope.component import getUtility

from zope.intid.interfaces import IIntIds

from z3c.relationfield.relation import RelationValue

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IDynamicType
from Products.Archetypes.Registry import registerField
from Products.Archetypes.public import ObjectField, ReferenceField
from Products.Archetypes import PloneMessageFactory as _
from Products.Archetypes.utils import DisplayList
from archetypes.z3crelationfield.interfaces import IZCRelationField

from plone.indexer import indexer


@indexer(IDynamicType)
def getIntId(obj):
    # do cool stuff
    intid_tool = getUtility(IIntIds)
    return intid_tool.getId(obj)


class ZCRelationField(ReferenceField):
    """A field for creating references from Archetypes objects to
    Dexterity objects.
    """
    implements(IZCRelationField)

    def get(self, instance, aslist=False, **kwargs):
        """
        """
        res = ObjectField.get(self, instance, **kwargs)
        if res is None:
            return res

        if self.multiValued:
            resolved = []
            for rel in res:
                resolved.append(rel.to_object)
        else:
            resolved = res.to_object
            if aslist:
                resolved = [resolved]

        return resolved

    def getRaw(self, instance, aslist=False, **kwargs):
        """
        """
        res = ObjectField.getRaw(self, instance, **kwargs)

        if self.multiValued:
            resolved = []
            for rel in res:
                resolved.append(rel.to_id)
        else:
            resolved = res.to_id
            if aslist:
                resolved = [resolved]

        return resolved

    def set(self, instance, value, **kwargs):
        """
        """
        if value is None:
            ObjectField.set(self, instance, value, **kwargs)
            return

        if self.multiValued and not isinstance(value, (list, tuple)):
            value = value,
        if isinstance(value, (list, tuple)) and not self.multiValued:
            raise ValueError(
                "Multiple values given for single valued field %r" % self)

        intid_tool = getUtility(IIntIds)

        #convert objects to intids if necessary
        if self.multiValued:
            result = []
            for v in value:
                if isinstance(v, (basestring, int)):
                    result.append(RelationValue(int(v)))
                else:
                    result.append(RelationValue(intid_tool.getId(v)))
        else:
            if isinstance(value, (basestring, int)):
                result = RelationValue(int(value))
            else:
                result = RelationValue(intid_tool.getId(value))

        ObjectField.set(self, instance, result, **kwargs)

    def _Vocabulary(self, content_instance):
        pairs = []
        pc = getToolByName(content_instance, 'portal_catalog')

        allowed_types = self.allowed_types
        allowed_types_method = getattr(self, 'allowed_types_method', None)
        if allowed_types_method:
            meth = getattr(content_instance, allowed_types_method)
            allowed_types = meth(self)

        skw = allowed_types and {'portal_type': allowed_types} or {}
        pc_brains = pc.searchResults(**skw)

        if self.vocabulary_custom_label is not None:
            label = lambda b: eval(self.vocabulary_custom_label, {'b': b})
        elif self.vocabulary_display_path_bound != -1 and len(
            pc_brains) > self.vocabulary_display_path_bound:
            at = _(u'label_at', default=u'at')
            label = lambda b: u'%s %s %s' % (
                self._brains_title_or_id(b, content_instance),
                                             at, b.getPath())
        else:
            label = lambda b: self._brains_title_or_id(b, content_instance)

        for b in pc_brains:
            pairs.append((str(b.intid), label(b)))

        if not self.required and not self.multiValued:
            no_reference = _(u'label_no_reference',
                             default=u'<no reference>')
            pairs.insert(0, ('', no_reference))

        __traceback_info__ = (content_instance, self.getName(), pairs)
        __traceback_info__  # pyflakes
        return DisplayList(pairs)


registerField(ZCRelationField, title='Relations',
              description='Used to set relationships between content.')
