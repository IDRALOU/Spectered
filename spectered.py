import importlib
import os

file_obf_name = input("Enter the name of obfuscated file: ")
content = open(file_obf_name).read()
content = content.replace("if __name__ == '__main__':", "")
content = content.replace("    Specter(__code__)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ,exec", "code_obj=")
content = content.replace(",globals()", "")

with open("to_deob.py", "w") as file:
    file.write(content)

from to_deob import code_obj

loader = importlib.machinery.SourceFileLoader('<py_compile>', file_obf_name)
source_bytes = loader.get_data(file_obf_name)
source_hash = importlib.util.source_hash(source_bytes)
bytecode = importlib._bootstrap_external._code_to_hash_pyc(code_obj, source_hash)

with open(f"to_deob2.pyc", "wb") as file:
    file.write(bytecode)

os.system("pycdc to_deob2.pyc > to_deob2.txt")
os.system("pycdas to_deob2.pyc > result.txt")

with open("result.txt") as file:
    lines = file.read().splitlines()
    for line in lines:
        if "                        16      LOAD_CONST              0: " in line:
            line_key = line.replace("                        16      LOAD_CONST              0: ", "")
            key = line_key.replace("b'", "").replace("'", "")

with open("to_deob2.txt") as file:
    lines = file.read().splitlines()
    n_v = lines[4].split(" = ")
    n_v[0] = n_v[0].replace("(", "").replace(")", "")
    n_v[1] = n_v[1].replace("(", "").replace(")", "")
    names = n_v[0].split(", ")
    values = n_v[1].split(", ")
    for name, value in zip(names, values):
        globals()[name] = value.replace("b'", "").replace("'", "")

codes_crypted = []
for line in lines[10:]:
    codes_crypted.append(line.replace("    ", "").replace(",", "").replace("])", ""))

code = ""

for code_crypted in codes_crypted:
    for l3 in globals()[code_crypted].split('\\x00'):
        if l3.isdigit():
            code += ''.join(chr(int(l3)-int(key)))

code = code.replace("\n", "").replace("\\n", "").replace("""# GG! You just deobfuscated Specter# https://github.com/billythegoat356/Specter# by billythegoat356# join discord.gg/plague for more Python tools!try:    if (        __author__ != "billythegoat356" or        __github__ != "https://github.com/billythegoat356/Specter" or        __discord__ != "https://discord.gg/plague" or        __license__ != "EPL-2.0" or        __code__ != "Hello world!" or        "Specter" not in globals() or        "Func" not in globals()    ):        int('skid')except:    input("You just executed a file obfuscated with Specter!Author: billythegoat356GitHub: https://github.com/billythegoat356/SpecterDiscord: https://discord.gg/plague")    __import__('sys').exit()    """, "")

code = "# Deobfuscated with Spectered (https://github.com/IDRALOU/Spectered)\n\n" + code + "\n# Deobfuscated with Spectered (https://github.com/IDRALOU/Spectered)"

with open("deob.py", "w", errors="ignore") as file:
    file.write(code)

os.remove("to_deob.py")
os.remove("to_deob2.pyc")
os.remove("to_deob2.txt")
os.remove("result.txt")

print()
input("Finished")
