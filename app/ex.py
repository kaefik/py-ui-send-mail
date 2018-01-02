import os
fl = os.path.exists("templates/data/sender_list/1")
base_dir = os.path.abspath(os.path.dirname(__file__))
print("fl = ",fl)
print(" base_dir = ",base_dir)

# os.rename("templates/data/sender_list/11","templates/data/sender_list/done/1")

if os.path.exists("templates/data/sender_list/done/1"):
    print(True)
else:
    print(False)

ar = os.path.split("templates/data/sender_list/done/1.txt")
print(ar)
print(ar[-1])