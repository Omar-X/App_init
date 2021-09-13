# ! /usr/bin/env python3
import os
import sys
# import shutil
from time import sleep

from default_values import *
from display import *
from buildozer_configure import *

img_exts = ["tif", "tiff", "jpg", "jpeg", "bmp", "gif", "png", "eps", "raw", "cr2", "nef", "orf", "sr2"]
font_exts = ["eot", "otf", "ttf", "fnt", "pfa", "woff", "woff2", "fot", "sfd", "vlw", "pfb", "gxf", "odttf", "fon",
             "etx", "chr", "ttc", "gdf", "gdr", "tpf", "acfm", "amfm", "dfont"]
sound_exts = ["pcm", "wav", "mpeg", "mp3", "aiff", "aac", "ogg", "wma", "alac", "flac", "wma", ""]
default_source_include_exts = ["py", "png", "jpg", "kv", "atlas"]
android_unsupported = ["pyaudio", "sounddevice", "soundfile", "ctypes"]


class Builder:
    path = ""
    order = ""
    app_folder = False
    title = ""

    @classmethod
    def run(cls):
        if not os.path.exists((cls.path + "/buildozer.spec")):
            buildozer_setup(Builder.path)
        for folder in ["Fonts", "Images", "Musics"]:
            if os.path.exists(cls.path + "/" + folder):
                normal_print(f"{folder} folder found")
            else:
                if cls.app_folder:
                    warning_print(f"{folder} folder does not exist")
                    normal_print(f"{folder} folder is important for organising projects")
                else:
                    normal_print(f"creating {folder}...")
                os.mkdir(cls.path + "/" + folder)
                head_print(f"{folder} created.")

        if cls.order == "start" or (cls.order in ["continue", "run"] and cls.app_folder):
            starting_point(Builder.path)
        elif cls.order == "continue":
            continuing_point(Builder.path)
        else:
            run_project(Builder.path)


def buildozer_setup(path):
    normal_print("Checking Buildozer ... ")
    check_init = os.system(f"cd {path}" + " ; " + "buildozer init")
    if check_init:
        warning_print("Buildozer not installed !!")
        normal_print("Installing installing Buildozer ...")
        os.system("pip3 install --user --upgrade buildozer")
        head_print("buildozer installed")
        check_init = os.system(f"cd {path}" + " ; " + "buildozer init")
        if not check_init:
            head_print("buildozer.spec created")
            normal_print("Need to update > sudo apt update ...")
            os.system("sudo apt update")
            head_print("Updated.")
        else:
            fail_print("An error occurred while installing buildozer.spec")
            sys.exit()


def starting_point(path):
    normal_print("building main.py")
    if os.path.exists(path + "/main.py"):
        print(bcolors.HEADER + "file exists" + bcolors.ENDC)
        continuing_point(path)

    else:  # setting up main.py and <project_name>.kv files
        normal_print("A template is going to be used")
        option = quest_input("Enter number of your option\n1>> ScreenManager(recommended)\n2>> Widget\n3>> None\n: ")
        project_name = os.path.basename(path)
        building_main(project_name, option, path)
        normal_print(f"Building {project_name}.kv file")
        building_kivy(project_name, option, path)
        # adding important files images and fonts
        continuing_point(path, True)
        # you forgot to add icon and presplash files
        ask = quest_input("Run main.py on your PC ? ['y'/'n']: ")
        if ask in ["Y", "y", "yes", "Yes"]:
            os.system(f"cd {path}" + " ; " + "python3 main.py")


def continuing_point(path, first_time=False):
    adding_files(path, Builder.app_folder)
    buildozer_conf = Buildozer_init(path)
    folders = ["Images", "Fonts", "Musics"]
    all_files = search_files(path)
    python_files = [x for x in all_files if x[-3:] == ".py"]
    kivy_files = [x for x in all_files if x[-3:] == ".kv"]

    # checking the title
    title = buildozer_conf.get_attributes("title")[0]
    if title.find("Application") != -1:
        warning_print(f"Your app name is {title}")
        title = quest_input(f"Enter the app name or press enter to continue with {title}\n:")
        if title:
            buildozer_conf.add_to("title", title, one_value=True)
            head_print(f"{title} added.")

    # Organizing the project
    for element in os.listdir(path):
        _, ext = os.path.splitext(element)
        ext = ext[1:]
        if ext in (img_exts + font_exts + sound_exts) and ext:
            if ext in img_exts:
                folder = folders[0]
            elif ext in font_exts:
                folder = folders[1]
            else:
                folder = folders[2]

            normal_print(f"Moving {element} to {folder} folder ...")  # problem here
            check = os.system(f"mv {path}/{element} {path}/{folder}/")
            check_file(element, folder, python_files)
            check_file(element, folder, kivy_files)
            head_print(f"{element} moved.") if not check else fail_print(f"Couldn't move {element}")

    # Adding extensions
    normal_print("Adding new extensions to buildozer.spec")
    exts = set(buildozer_conf.get_extensions())
    default_source_include_exts = set(buildozer_conf.get_attributes("source.include_exts"))
    default_source_include_exts.update(["spec"])
    exts.difference_update(default_source_include_exts)
    if first_time:
        buildozer_conf.add_to("source.include_exts", exts)
    elif exts:
        request = quest_input(f"The following extensions {exts} will be added to buildozer.spec"
                              f"\nenter the extensions you with to discard like: ext_1, ext_2, ext3 "
                              f"\nor press 'Enter' to continue \n\t or 'n' to quit \n: ")
        if request and request not in ["n", "N"]:
            request = (request.replace(" ", "")).split(",")
            exts.difference_update(request)
            buildozer_conf.add_to("source.include_exts", exts)
            head_print("Extensions added")
        elif not request:
            buildozer_conf.add_to("source.include_exts", exts)
            head_print("Extensions added")
    else:
        normal_print("No new extensions need to be added")

    # Adding modules to buildozer
    request = True if (first_time or quest_input("press 'y' to process and add your modules or anything"
                                                 " to continue\n: ") in ['y', "Y"]) else False

    if request:
        modules = set()
        for file in python_files:
            modules.update(get_modules(file))
        buildozer_conf.add_to("requirements", modules)

    # add icon and presplash files here
    added_once = [False, False]
    icon_field = buildozer_conf.get_attributes("icon.filename", False)[0]
    presplash_field = buildozer_conf.get_attributes("presplash.filename", False)[0]
    for i in os.listdir(f"{path}/Images"):
        if i[:5] == "icon." and not added_once[0]:
            if icon_field[-14:] != "/data/icon.png" and f"s/Images/{i}" in icon_field:
                added_once[0] = True
                continue
            attribute = "%(source.dir)s/" + "Images/" + i
            buildozer_conf.add_to("icon.filename", attribute, True)
            head_print(f"{i} image added.")
            added_once[0] = True
        elif i[:10] == "presplash." and not added_once[1]:
            if presplash_field[-19:] != "/data/presplash.png" and f"s/Images/{i}" in presplash_field:
                added_once[1] = True
                continue
            attribute = "%(source.dir)s/" + "Images/" + i
            buildozer_conf.add_to("presplash.filename", attribute, True)
            head_print(f"{i} image added.")
            added_once[1] = True

    # run project
    if not first_time and not Builder.app_folder:
        ask = quest_input("build/run application ? ['y'/'n']: ")
        if ask in ["Y", "y", "yes", "Yes"]:
            run_project(path)


def run_project(path):
    request_dict = {
        "1": "buildozer -v android debug",
        "2": "buildozer android deploy run logcat",
        "3": "buildozer android clean",
        "4": "python3 main.py"
                    }
    while True:
        request = quest_input("choose option: \t(Like: 1,2)\n1>> Build the application in debug mode."
                              "\n2>> Deploy and Run the application on the device. (device must be connected)"
                              "\n3>> Clean the target environment."
                              "\n4>> Run main.py on your PC"
                              "\n: ")
        request = (request.replace(" ", "")).split(",")
        request = sorted(set([x for x in request if (x.isdigit() and 0<int(x)<5)]), key=request.index)
        ask = quest_input(f"Continue with {request}? [y/n]:")
        if ask in ["Y", "y", "yes", "Yes"] and request:
            break
    for req in request:
        if req == "2" and not os.path.exists(f"{path}/bin"):
            warning_print("You need to build app first.")
            ask = quest_input("Build app ? ['y'/'n']: ")
            if ask in ["Y", "y", "yes", "Yes"]:
                os.system(f"cd {path}" + " ; " + request_dict["1"])
            else:
                break
        os.system(f"cd {path}" + " ; " + request_dict[req])


def check_file(file, folder, files_list):
    for i in files_list:
        normal_print(f"Searching for {file} in {i} to edit ...")
        text = open(f"{i}", "r").read()
        if text.find(f"{file}") == -1:
            normal_print(f"file: {file} wasn't mentioned in {i}")
        else:
            normal_print(f"file: {file} was mentioned in {i}")
            ask = quest_input(f"press 'y' to edit {i} (replacing {file} with {folder}/{file})\n:")
            if ask in ["y", "Y"]:
                text = text.replace(f"{file}", f"{folder}/{file}")
                open(f"{i}", "w").write(text)
                head_print("Replaced.")


def adding_files(path, app_folder=False):
    normal_print("Searching for modernpics.otf ...")
    if os.path.exists(f"{path}/Fonts/modernpics.otf"):
        normal_print("modernpics.otf found.")
    elif not app_folder and os.path.exists(f"{path}/modernpics.otf"):
        normal_print("modernpics.otf found.")
        normal_print("Moving modernpics.otf Fonts folder ...")
        os.system(f"mv {path}/modernpics.otf {path}/Fonts")
        head_print("Moved.")
    else:
        normal_print(f"Adding modernpics.otf to {path} ...")
        check = os.system(f"cp {default_path}static/modernpics.otf {path}/Fonts/")  # use shutile
        head_print("modernpics.otf added.") if not check else fail_print("Couldn't move modernpics.otf")

    normal_print("Searching for ArialUnicodeMS.ttf ...")
    if os.path.exists(f"{path}/Fonts/ArialUnicodeMS.ttf"):
        normal_print("ArialUnicodeMS.ttf found.")
    elif not app_folder and os.path.exists(f"{path}/ArialUnicodeMS.ttf"):
        normal_print("ArialUnicodeMS.ttf found.")
        normal_print("Moving ArialUnicodeMS.ttf to Fonts folder ...")
        os.system(f"mv {path}/ArialUnicodeMS.ttf {path}/Fonts")
        head_print("Moved.")
    else:
        normal_print(f"Adding ArialUnicodeMS.ttf to {path} ...")
        check = os.system(f"cp {default_path}static/ArialUnicodeMS.ttf {path}/Fonts/")  # use shutile
        head_print("modernpics.otf added.") if not check else fail_print("Couldn't move modernpics.otf")

    normal_print("Searching for Icon image ...")
    if "icon" in [x[:4] for x in os.listdir(f"{path}/Images")]:
        normal_print("icon image found")

    elif not app_folder and "icon" in [x[:4] for x in os.listdir(f"{path}")]:
        normal_print("icon image found.")
        normal_print("icon will be moved to Images folder...")

    else:
        warning_print("icon image needed, a temporary one will be added, you can replace it.")
        warning_print("when replacing make sure that name is icon.<png/jpg/jpeg/etc>.")
        sleep(5)
        normal_print(f"Adding icon.png to {path}/Images/ ...")
        check = os.system(f"cp {default_path}static/icon.png {path}/Images/")  # use shutile
        head_print("icon.png added.") if not check else fail_print("Couldn't move icon.png")

    normal_print("Searching for Presplash image ...")
    if "presplash" in [x[:9] for x in os.listdir(f"{path}/Images")]:
        normal_print("Presplash image found")
    elif not app_folder and "presplash" in [x[:9] for x in os.listdir(f"{path}")]:
        normal_print("presplash image found.")
        normal_print("presplash will be moved to Images folder...")
    else:
        warning_print("Presplash image needed, a temporary one will be added, you can replace it.")
        warning_print("when replacing make sure that name is Presplash.<png/jpg/jpeg/etc>.")
        sleep(5)
        normal_print(f"Adding Presplash.png to {path}/Images/ ...")
        check = os.system(f"cp {default_path}static/presplash.png {path}/Images/")  # use shutil
        head_print("Presplash.png added.") if not check else fail_print("Couldn't move Presplash.png")

    if os.path.exists("Musics/pristine-609.mp3"):
        normal_print("pristine-609.mp3 found.")
    else:
        normal_print("adding a defult sound file to Musics folder ...")
        check = os.system(f"cp {default_path}static/pristine-609.mp3 {path}/Musics/")  # use shutil
        head_print("pristine-609.mp3 added.") if not check else fail_print("Couldn't move pristine-609.mp3")


def building_main(name, option, path):
    with open(path + "/main.py", "w+") as main_py:  # adding helpful codes to main.py
        head_print("main.py built.")
        normal_print("Writing in main.py ...")
        main_text = open(f"{default_path}main_py_default", "r").read()  # not finished
        if option == '1':
            main_text = main_text.format("from kivy.uix.screenmanager import ScreenManager", "ScreenManager",
                                         name=name.upper(),
                                         rise_keyboard="{'d': .2, 't': 'in_out_expo'}")
        elif option == "2":
            main_text = main_text.format("from kivy.uix.widget import Widget", "Widget", name=name.upper(),
                                         rise_keyboard="{'d': .2, 't': 'in_out_expo'}")
        else:
            main_text = ""
        main_py.write(main_text)

    head_print("main.py initialized.")


def building_kivy(name, option, path):
    with open(f"{path}/{name}.kv", "w") as kivy_file:  # setting kivy file
        main_text = open(f"{default_path}project_kv.txt", "r").read()
        if option in ["1", "2"]:
            if option == "1":
                start = main_text.find("{{start_screenmanager}}") + 23
                end = main_text.find("{{end_screenmanager}}")
            else:
                start = main_text.find("{{start_widget}}") + 16
                end = main_text.find("{{end_widget}}")
            kivy_file.write(main_text[start:end])

        else:
            kivy_file.write("")
    head_print(f"{name} initialized.")


def search_files(folder_path):  # a problem here
    my_results = set()
    other_folder = [folder_path]
    x, b = 0, 0
    while b <= x:
        try:
            for i in os.listdir(other_folder[b]):
                if i[0] not in [".", "bin"]:
                    unknown = os.path.join(other_folder[b], i)
                    if os.path.isdir(unknown):
                        other_folder.append(unknown)
                        x += 1
                    else:
                        my_results.add(unknown)
            b += 1
        except:
            b += 1

    return my_results


def get_modules(path):
    modules = set()
    normal_print("reading modules in your project")
    normal_print("after that modules will be added to your buildozer.spec")
    text_lines = open(path, "r").readlines()
    for line in text_lines:
        if "#" in line:
            line = line[:line.find("#")]
        if "import" in line or "from" in line:  # not complete
            # deleting any possible indentation and \n
            for b, k in enumerate(line[:-1]):
                if k in [" ", "\t"]:
                    continue
                else:
                    line = line[b:]
                    break
            line = line.replace("\n", "")

            # reading module
            line = (line.split(" "))[1]
            # in case module is a folder
            line = line.split(".")
            if len(line[0].split(",")) <= 1:
                module = line[0]
                if module not in default_modules and module != "kivy" and module not in modules:
                    head_print(f"New Module found {module}")
                    modules.add(module)
            else:
                for module in line[0].split(","):
                    if module not in default_modules and module != "kivy" and module not in modules:
                        head_print(f"New Module found {module}")
                        modules.add(module)

    if len(modules):
        normal_print("Looking for requirements for each new module")
        modules.update(deep_modules(list(modules)))
        modules.difference_update(default_modules)
        warning_print("Not all modules can be used check if they import ctypes module or not \n\tas they uses"
                      " shared_libraries which isn't supported")
        normal_print("checking modules")
        for i in android_unsupported:
            if i in modules:
                warning_print(f"you can't use this module \"{i}\" android doesn't support it")
                sleep(4)
        warning_print("not all modules has been checked, report us if you found something.")
        modules.difference_update(android_unsupported)
        normal_print(f"final list of modules: {modules}")
    else:
        normal_print("NO new modules are needed")
    return modules


def deep_modules(modules):
    final_modules = []
    for module in modules:
        normal_print(f"Analyzing {module} ...")
        try:
            requires = (os.popen(f"pip3 show {module}").readlines())[-2]
            requires = ((requires[9:-1]).replace(" ", "")).split(",")
        except:
            print("error")
            requires = ['']

        if requires[0]:
            warning_print(f"{module.title()} has some requires: {requires}")
            final_modules = requires + deep_modules(requires)

    return final_modules
