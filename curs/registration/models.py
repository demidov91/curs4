from neomodel import StructuredNode, StringProperty, RelationshipTo,\
 BooleanProperty, IntegerProperty
    
class Userprofile(StructuredNode):
    is_client = BooleanProperty(default=False)
    user_id = IntegerProperty(index=True)
    knows = RelationshipTo('Userprofile', 'KNOWS')
    raw_email = StringProperty()