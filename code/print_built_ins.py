# <https://
# Prints all built-in property names into a file

from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands

built_ins = acc.GetAllPropertyNames()
with open('built_ins_list.txt', 'w') as f:
    print(built_ins, file=f)
