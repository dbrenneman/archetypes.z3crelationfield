from zc.relation.interfaces import ICatalog
from z3c.relationfield.index import RelationCatalog
from five.intid.site import addUtility


def add_relations(context):
    addUtility(context, ICatalog, RelationCatalog, ofs_name='relations',
               findroot=False)


def installRelations(context):
    if context.readDataFile('install_relations.txt') is None:
        return
    portal = context.getSite()
    add_relations(portal)
    return "Added relations utility."
