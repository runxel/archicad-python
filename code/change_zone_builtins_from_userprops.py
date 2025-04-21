# Schreibt aus zwei Benutzereigenschaften die nativen Raumnamen und -nummern.
# Die Eigenschaften können sogar Berechnungen sein!
# BOML | @runxel · 2022
# v1.0

from archicad import ACConnection
from archicad.releases import Commands, Types, Utilities

conn = ACConnection.connect()
if not conn:
	raise Exception("No Archicad instance running!")

acc: Commands = conn.commands
acu: Utilities = conn.utilities
act: Types = conn.types


# Alle Räume auswählen (gibt GUIDs zurück)
elem_all_zones = acc.GetElementsByType("Zone")

# Enthält die GUID der angefragten Eigenschaft (Built-ins; non-localized)
prop_zname = acu.GetBuiltInPropertyId("Zone_ZoneName")
prop_znumber = acu.GetBuiltInPropertyId("Zone_ZoneNumber")

# Benutzereigenschaft (localized): 'Gruppe', 'Eigenschaftsname'
# HIER ANPASSEN AN EIGENE BEDÜRFNISSE !
prop_pname = acu.GetUserDefinedPropertyId("Allgemeine Werte", "Raumname")
prop_pnumber = acu.GetUserDefinedPropertyId("Allgemeine Werte", "Raumnummer")


# Gibt eine Liste mit den entsprechenden Eigenschaften der Elemente zurück
# List comprehension, ein netter Python-Trick
propvallist_pname = [
	val.propertyValues[0].propertyValue.value
	for val in acc.GetPropertyValuesOfElements(elem_all_zones, [prop_pname])
]
propvallist_pnumber = [
	val.propertyValues[0].propertyValue.value
	for val in acc.GetPropertyValuesOfElements(elem_all_zones, [prop_pnumber])
]

for i, elem in enumerate(elem_all_zones):
	new_zonename = act.ElementPropertyValue(
		elem.elementId, prop_zname, act.NormalStringPropertyValue(propvallist_pname[i])
	)
	new_zonenumber = act.ElementPropertyValue(
		elem.elementId,
		prop_znumber,
		act.NormalStringPropertyValue(propvallist_pnumber[i]),
	)
	# Zurückspielen der Eigenschaften
	acc.SetPropertyValuesOfElements([new_zonename, new_zonenumber])
