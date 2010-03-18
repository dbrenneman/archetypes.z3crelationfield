from Products.Archetypes import atapi

from Products.CMFCore import utils as cmfutils
from demo import ZCRelationFieldDemoContent


def initialize(context):
    """Intializer called when used as a Zope 2 product."""
    # Retrieve the content types that have been registered with Archetypes
    # This happens when the content type is imported and the registerType()
    # call in the content type's module is invoked. Actually, this happens
    # during ZCML processing, but we do it here again to be explicit. Of
    # course, even if we import the module several times, it is only run
    # once.

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes('archetypes.z3crelationfield'),
        'archetypes.z3crelationfield')

    # Now initialize all these content types. The initialization process takes
    # care of registering low-level Zope 2 factories, including the relevant
    # add-permission. These are listed in config.py. We use different
    # permissions for each content type to allow maximum flexibility of who
    # can add which content types, where. The roles are set up in rolemap.xml
    # in the GenericSetup profile.

    for atype, constructor in zip(content_types, constructors):
        cmfutils.ContentInit('%s: %s' % ('archetypes.z3crelationfield', atype.portal_type),
            content_types      = (atype, ),
            permission         = 'Add portal content',
            extra_constructors = (constructor,),
            ).initialize(context)

