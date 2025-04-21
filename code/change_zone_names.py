# Extends on the simple example shown in "change_zone_name.py"
# 	for more complex situations, where you want to swap a whole lot of names.
# license: BOML • @runxel 2025
# v1.0

from archicad import ACConnection
from archicad.releases import Commands, Types, Utilities

conn = ACConnection.connect()
if not conn:
	raise Exception("No Archicad instance running!")

acc: Commands = conn.commands
acu: Utilities = conn.utilities
act: Types = conn.types


# The following list will act as an 1:1 replacement.
# Items that are not in this list just stay as they are.
REPLACE_LIST = {
	"Wohnen": "Main Room",
	"Schlafen": "Bedroom",
	"Bad": "Bathroom",
	"Küche": "Kitchen",
}


def constructStringPropertyValue(
	elementId: Types.ElementId,
	propertyID: Types.PropertyId,
	string: str,
) -> Types.PropertyValue:
	"""Construct a valid string-based PropertyValue."""
	pval = act.ElementPropertyValue(
		elementId, propertyID, act.NormalStringPropertyValue(string)
	)
	return pval


def replace(match: str, dictionary: dict) -> str:
	"""Takes a string and matches it against a list (dictionary).\n
	If an occurence is found it will return the value of the key (input)."""
	for key in dictionary.keys():
		if match in key:
			return dictionary.get(key)
	return match


# get all zones
elements = acc.GetElementsByType("Zone")

# get the GUID of the requested property
propertyID = acu.GetBuiltInPropertyId("Zone_ZoneName")

# returns a list of all the property values of the elements in question
propval_list = acc.GetPropertyValuesOfElements(elements, [propertyID])


for i, elem in enumerate(elements):
	curr_zone_name = propval_list[i].propertyValues[0].propertyValue.value
	acc.SetPropertyValuesOfElements(
		[
			constructStringPropertyValue(
				elem.elementId, propertyID, replace(curr_zone_name, REPLACE_LIST)
			)
		]
	)
