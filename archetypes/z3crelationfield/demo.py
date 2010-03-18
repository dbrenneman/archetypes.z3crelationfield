from Products.Archetypes.public import ReferenceWidget, Schema, registerType
from archetypes.z3crelationfield.field import ZCRelationField

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeBaseSchema


class ZCRelationFieldDemoContent(ATCTContent):
    """ A demo content type using ZCRelationField.
    """
    meta_type = 'ZCRelationFieldDemoContent'
    portal_type = 'ZCRelationFieldDemoContent'

    schema = ATContentTypeBaseSchema.copy() + Schema((
        ZCRelationField(
            'zcrelations',
            role='Owner',
            relationship='foo',
            widget=ReferenceWidget(
                label='ZC Relations',
            ),
        ),
    ))


registerType(ZCRelationFieldDemoContent, 'archetypes.z3crelationfield')
