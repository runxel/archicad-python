# This script will rename all Layouts in a given folder to their first placed drawing.
# It is currently impossible to tell what kind of drawing is placed
# on a layout! So this will cover internal drawings as well as external PDFs.
# license: BOML • @runxel 2025-03-30
# v1.0 • tested in AC28
# name_layout_by_content.py
# for https://community.graphisoft.com/t5/Documentation/Replace-Name-Layout-With-Drawing-Name-in/m-p/657506

from archicad import ACConnection
from archicad.releases import Commands, Types, Utilities

conn = ACConnection.connect()
if not conn:
	raise Exception("No Archicad instance running!")

acc: Commands = conn.commands
acu: Utilities = conn.utilities
act: Types = conn.types

subset_name = "TEST folder"
# rename :	  ^^^^^^^^^^^^
# It is probably good advice to limit the extent of this script, since –as stated above–
# we can not know the kind of placed drawing.
# Run the script wisely!
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
