# Prints all built-in property names into a file

from archicad import ACConnection

TO_FILE = False


conn = ACConnection.connect()
assert conn

acc = conn.commands

built_ins = acc.GetAllPropertyNames()

if TO_FILE:
	with open("built_ins_list.txt", "w") as f:
		print(built_ins, file=f)
else:
	for bi in built_ins:
		if bi.type == "BuiltIn":
			print(bi)
