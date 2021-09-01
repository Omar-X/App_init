import os, sys, main
from display import *
import soundfile

system = sys.platform.lower()
if system != "linux":
    fail_print("Your system isn't supported at the moment \n buildozer can't be installed")
    sys.exit()


def main_func(argv, path=None):
    # building up a project
    if argv not in ["start", "Start", "continue", "Continue", "Run", "run"]:
        path = "path" + "/" + "<new project name>"
        if argv.find("help") == -1 or argv.find("-h") == -1:
            fail_print("Wrong entry")
            warning_print("Use one of these options > start, continue, run")
            normal_print("Example > it should be like")
        print(bcolors.HEADER + "Python3 start " + path + bcolors.ENDC)
        sys.exit()

    elif argv == "start" or argv == "Start":
        # working on path folder
        if not path:
            normal_print(f"Enter path for new project like {os.getcwd()}/<project_name>")
            path = quest_input("Folder path: ")
        normal_print("Checking folder path ...")
        if os.path.exists(path):
            normal_print("Path exists")
            main.Builder.app_folder = True
        else:
            warning_print("Path does not exist")
            normal_print(f"Creating {path} folder")
            while True:
                try:
                    os.mkdir(path)
                    normal_print("Folder Created.")
                    break
                except Exception as e:
                    print(f"{bcolors.FAIL}{e[0:11]}{bcolors.ENDC}{e[11:]}")
                    print("Try again.")
                    path = input(f"{bcolors.OKCYAN}folder path: {bcolors.OKCYAN}")
                    continue

    else:
        if not path:
            normal_print(f"Enter path for the project like {os.getcwd()}/<project_name>")
            path = quest_input("Folder path: ")
        normal_print("Checking folder path ...")
        while True:
            if os.path.exists(path):
                normal_print("Path exists")
                break
            else:
                warning_print("Path does not exist try again.")
                path = input("Folder path: ")
                continue

    main.Builder.title = os.path.basename(path)
    main.Builder.path = path
    main.Builder.order = argv.lower()
    main.Builder.run()


if __name__ == "__main__":
    main_func(sys.argv[1], sys.argv[2])
# import main
