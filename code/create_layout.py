# Simplest example for creating a Layout in Archicad
# BOML | runxel 2020
# v1.0 | works in ac24.b3008
# create_layout.py
# for <https://archicad-talk.graphisoft.com/viewtopic.php?f=23&t=70570#p315412>

from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities


#### some basic config ####
master_name = "A2 Querformat"  # the Master Layout you want to use
parent_name = "Parent"  # Parent folder name

lname = "New Layout"  # Name of the layout to be created
# DIN A2 format size; always millimeter
lhor = 594
lvert = 420
lmargin_left = lmargin_top = lmargin_right = lmargin_bottom = 0
# Declare the appropiate Layout Parameters (see API for more info)
lparam = act.LayoutParameters(
	lhor,
	lvert,
	lmargin_left,
	lmargin_top,
	lmargin_right,
	lmargin_bottom,
	"",
	False,
	False,
	False,
	1,
	1,
	"",
	"",
	False,
	False,
)
# which tree to checkout: 'LayoutBook', 'PublisherSets', 'ViewMap'
root_tree_loc = "LayoutBook"

# Retrieve the Root Item
layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(root_tree_loc))

# Now slightly weird stuff:
# For the FindInNavigatorItemTree function we need a criteria function, which gets called
#  with the item to check as only parameter.
# We will then automatically loop over all items in the defined tree.
# In this function we can decide if the current item adheres to our criteria,
#  if so, we will return true.


def findMaster(item: act.NavigatorItem):
	return True if item.name == master_name else False


def findParent(item: act.NavigatorItem):
	return True if item.name == parent_name else False


list_master = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, findMaster)
list_parent = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, findParent)

lmaster = list_master[0].navigatorItemId
lparent = list_parent[0].navigatorItemId


# Now actually create the Layout; returns a GUID on `new_layout`
new_layout = acc.CreateLayout(lname, lparam, lmaster, lparent)
