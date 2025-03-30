# This script will rename all Layouts in a given folder to their first placed drawing.
# It is currently impossible to tell what kind of drawing is placed
# on a layout! So this will cover internal drawings as well as external PDFs.
# license: BOML • @runxel 2025-03-30
# v1.0 • tested in AC28
# name_layout_by_content.py
# for <https://community.graphisoft.com/t5/Documentation/Replace-Name-Layout-With-Drawing-Name-in/m-p/657506>

import archicad

try:
	conn = archicad.ACConnection.connect()
	assert conn

	acc = conn.commands
	act = conn.types
	acu = conn.utilities

except AssertionError:
	raise RuntimeError("No Archicad instance running!")


subset_name = "TEST folder"
# rename :	  ^^^^^^^^^^^^
# ------------------------- #

layoutBookTree = acc.GetNavigatorItemTree(act.NavigatorTreeId("LayoutBook"))

# get the approppiate Folder:
subset_itemList = acu.FindInNavigatorItemTree(
	layoutBookTree.rootItem, lambda node: node.name == subset_name
)

# The following gives not the subset as-is, but instead a list of
# discrete 'NavigatorItemArrayItem's (sic)...
for item in subset_itemList[0].children:
	# is a Drawing placed?
	if item.navigatorItem.children is not None:
		acc.RenameNavigatorItem(
			item.navigatorItem.navigatorItemId,
			item.navigatorItem.children[0].navigatorItem.name,
		)
