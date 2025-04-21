# Simple example on how to change a Zone name.
# license: BOML • @runxel 2020
# v1.0
# for https://community.graphisoft.com/t5/Archicad-Python-API/Changing-Zone-name-using-Python/td-p/267090

from archicad import ACConnection
from archicad.releases import Commands, Types, Utilities

conn = ACConnection.connect()
if not conn:
	raise Exception("No Archicad instance running!")

acc: Commands = conn.commands
acu: Utilities = conn.utilities
act: Types = conn.types


# get all zones, assign to `elements`
elements = acc.GetElementsByType("Zone")

# prop now holds the GUID of the requested property
prop = acu.GetBuiltInPropertyId("Zone_ZoneName")

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
			elem.elementId, prop, act.NormalStringPropertyValue(zonename_new)
		)
		# set the zone name
		acc.SetPropertyValuesOfElements([new_val])
