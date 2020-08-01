# Simple example on how to change a zone name
# BOML | runxel 2020
# v1.0
# for <https://archicad-talk.graphisoft.com/viewtopic.php?f=23&t=70399#p314406>

from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

# get all zones, assign to `elements`
elements = acc.GetElementsByType('Zone')

# prop now holds the GUID of the requested property
prop = acu.GetBuiltInPropertyId('Zone_ZoneName')

# returns a list of all the property values of the elements in question
propval_list = acc.GetPropertyValuesOfElements(elements, [prop])

# replace all occurrences of the first string with the second one
#  (this is just a very basic example, of course you could do
#   much more sophisticated versions)
zonename_to_replace = "Wohnen"
zonename_new = "Main Room"


for i, elem in enumerate(elements):
    # propstr holds the actual string of the current zone name
    propstr = propval_list[i].propertyValues[0].propertyValue.value
    # check if we got a match
    if propstr == zonename_to_replace:
        # if so, construct a new prop value
        new_val = act.ElementPropertyValue(
            elem.elementId, prop, act.NormalStringPropertyValue(zonename_new))
        # set the zone name
        acc.SetPropertyValuesOfElements([new_val])
