class bcolors:
    HEADER = '\033[95m'  # Purple
    OKBLUE = '\033[94m'  # Blue
    OKCYAN = '\033[96m'  # Light Blue
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'  # Red
    GRAY = '\033[90m'  # gray
    ENDC = '\033[0m'  # Normal
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# print(f"{bcolors.WARNING} ~~ text ~~ {bcolors.ENDC}")


def _standard(text, text_type, head_color, text_color=bcolors.OKGREEN):
    print(f"[{head_color}{text_type.upper()}{bcolors.ENDC}]: {text_color}{text}{bcolors.ENDC}.")


def warning_print(text, text_color=bcolors.OKGREEN):
    _standard(text, "warning", bcolors.WARNING, text_color)


def normal_print(text, text_color=bcolors.OKCYAN):
    _standard(text, "info", bcolors.OKCYAN, text_color)


def fail_print(text, text_color=(bcolors.FAIL + bcolors.BOLD)):
    _standard(text, "error", bcolors.FAIL, text_color)


def head_print(text, text_color=bcolors.HEADER + bcolors.BOLD):
    _standard(text, "DONE", bcolors.HEADER, text_color)


def quest_input(text):
    request = input(f"[{bcolors.HEADER}Input{bcolors.ENDC}]: {bcolors.OKBLUE + bcolors.BOLD}{text}{bcolors.HEADER}")
    print(f"{bcolors.ENDC}")
    return request
