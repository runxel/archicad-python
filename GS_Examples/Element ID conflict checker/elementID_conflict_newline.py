# example of Graphisoft modified by Lucas Becker
# for https://forum.graphisoft.de/viewtopic.php?f=26&t=27212&p=157522#p157522
from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

################################ CONFIGURATION #################################
elements = acc.GetAllElements()
messageWhenNoConflictFound = "There is no elementID conflict."
conflictMessageParts = ["[Conflict]", "elements have", "as element ID:\n"]

def GetConflictMessage(elementIDPropertyValue, elementIds):
    elem_str = ("\n".join(map(str, sorted(elementIds, key=lambda id: id.guid))))
    return f"{conflictMessageParts[0]} {len(elementIds)} {conflictMessageParts[1]} '{elementIDPropertyValue}' {conflictMessageParts[2]}" + elem_str
################################################################################

elementIdPropertyId = acu.GetBuiltInPropertyId('General_ElementID')
propertyValuesForElements = acc.GetPropertyValuesOfElements(elements, [elementIdPropertyId])

propertyValuesToElementIdsDictionary = {}
for i in range(len(propertyValuesForElements)):
    elementId = elements[i].elementId
    propertyValue = propertyValuesForElements[i].propertyValues[0].propertyValue.value
    if propertyValue not in propertyValuesToElementIdsDictionary:
        propertyValuesToElementIdsDictionary[propertyValue] = set()
    propertyValuesToElementIdsDictionary[propertyValue].add(elementId)

noConflictFound = True
for k, v in sorted(propertyValuesToElementIdsDictionary.items()):
    if len(v) > 1:
        noConflictFound = False
        print(GetConflictMessage(k, v))

if noConflictFound:
    print(messageWhenNoConflictFound)
