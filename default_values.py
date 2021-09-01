import os

# getting path so you can run the script python3 App_init, python3 .
if os.getcwd()[-8:] != "App_init":
    default_path = "App_init/"
    print(default_path)
else:
    default_path = ""

# reading all built in modules
default_modules = open(f"{default_path}default_modules.txt", "r").readlines()
for a, i in enumerate(default_modules):
    if i[0] != "#":
        # make a list of all names
        default_modules[a] = i.replace("\n", "")
        default_modules[a] = default_modules[a].replace(" ", "")
    # removing all comments
for i in default_modules:
    if i[0] == "#":
        default_modules.remove(i)


