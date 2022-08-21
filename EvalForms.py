# stdlib.
from hashlib import md5
from os import listdir, system
from os.path import isfile, splitext
from typing import TextIO



# NOTE:
# You should edit a few variables below to adapt the script to your project.
# form_dir      Edit this to reflect the directory containing ALL of your project's *.ui files.
# cli_out       Set this to true if you desire info printed in the terminal.
# - zspinelli

FORM_DIR: str = "gui"
CLI_OUT: bool = False

list_path: str = f"{FORM_DIR}/hash_list.txt"
_list_file = None
_hashes: dict[str, str] = {}     # {form_path : hash_value}



def _condPrintInfo(p_message: str) -> None:
    # Print info if user desires.

    # User set CLI_OUT to True.
    if CLI_OUT: print(p_message)



# ---- Gather any previous hashes. ---- #

# Hash list file exists.
if isfile(list_path):
    LINEPART_FILENAME: int = 0
    LINEPART_HASHVALUE: int = 1

    _condPrintInfo("Using existing hash_list file.")

    list_file = open(list_path, "r")
    file_lines: list[str] = list_file.readlines()

    _condPrintInfo(f"hash_list length: {len(file_lines)}\n")

    # ---- Build a dictionary of found hashes. ---- #

    _condPrintInfo("Hashes:")

    for line in file_lines:
        _condPrintInfo(line.strip())

        line_parts: list[str] = line.strip().split(":")
        _hashes.update({line_parts[LINEPART_FILENAME] : line_parts[LINEPART_HASHVALUE]})

    # ---- Delete records referring to nonexistent forms. ---- #

    dead_forms: list[str] = []

    for form in _hashes:
        # Form file exists.
        if not isfile(f"{FORM_DIR}/{form}"):
            dead_forms.append(form)

    for form in dead_forms:
        del _hashes[form]



# --- Hash new forms, modified forms, and recompile deleted scripts --- #

_condPrintInfo("\nAnalyzing forms...")

for form in listdir(FORM_DIR):
    # File looks like a Qt ui form.
    if splitext(form)[1] == ".ui":
        _condPrintInfo(f"\n{'Form:':<8}{form}")

        form_file: TextIO = open(f"{FORM_DIR}/{form}", "r")
        form_data: bytes = form_file.read().encode("utf-8")
        form_file.close()

        hash_value: str = md5(form_data).hexdigest()
        _condPrintInfo(f"{'Hash:':<8}{hash_value}")

        # Form has previous and identical hash.
        if form in _hashes and _hashes[form] == hash_value:
            _condPrintInfo("Hash identical.")

        # Form is new or hashed before.
        else:
            _condPrintInfo("Form produced new hash.")
            system(f"pyside6-uic {FORM_DIR}/{form} > {FORM_DIR}/{splitext(form)[0]}.py")
            _hashes.update({form: hash_value})



# ---- Write out the hash collection. ---- #

# List file not open.
if not _list_file:
    _list_file = open(list_path, "w")

first_line: bool = True

for form in _hashes:
    # Writing first line.
    if first_line:
        _list_file.write(f"{form}:{_hashes[form]}")
        first_line = False

    # Writing more lines.
    else:
        _list_file.write(f"\n{form}:{_hashes[form]}")



# ---- Close hash list and notify completion. ---- #

_list_file.close()
_condPrintInfo("\nForm evaluation complete.\n")
