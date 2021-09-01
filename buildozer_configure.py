# from display import *
import os


class Buildozer_init:

    def __init__(self, path):
        self.path = path

    def get_extensions(self):  # to add them later to buildozer.spec
        my_results = set()
        other_folder = [self.path]
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
                            _, ext = os.path.splitext(i)
                            my_results.add(ext[1:])
                b += 1
            except:
                b += 1
        return my_results

    def add_to(self, field_name, attributes, one_value=False):  # not precise
        # reading buildozer
        spec_lines, field_line_nu = self.get_field(field_name)
        field_line = spec_lines[field_line_nu]

        # adding the attributes
        equal_sign = field_line.find("=")
        equal_sign += 1
        if type(attributes) == list or type(attributes) == set:
            for i in attributes:
                field_line = field_line[:equal_sign + 1] + i + "," + field_line[equal_sign + 1:]
        elif not one_value:
            field_line = field_line[:equal_sign + 1] + attributes + "," + field_line[equal_sign + 1:]
        else:
            field_line = field_line[:equal_sign + 1] + attributes
        spec_lines[field_line_nu] = field_line
        open(f"{self.path}/buildozer.spec", "w").writelines(spec_lines)

    def get_attributes(self, field_name, remove_window=True):
        spec_lines, field_line_nu = self.get_field(field_name, remove_window)
        field_line = spec_lines[field_line_nu]
        equal_sign = field_line.find("=")
        end_sign = field_line.find("\n")
        values = (field_line[equal_sign + 1: end_sign]).replace(" ", "")
        values = values.split(",")
        return values

    def get_field(self, field_name, remove_window=True):
        # reading buildozer.spec
        spec_lines = open(f"{self.path}/buildozer.spec", "r").readlines()
        # getting the line which contains that field
        field_line_nu = -1

        for nu, i in enumerate(spec_lines):
            if field_name in i[:len(field_name) + 5] and "=" in i:
                field_line_nu = nu
                break
        # see if that field closed #
        field_line = spec_lines[field_line_nu]
        if remove_window and spec_lines[field_line_nu][0] == "#":
            field_line = field_line[1:]
            spec_lines[field_line_nu] = field_line
        return spec_lines, field_line_nu
