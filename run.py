variables = {}
functions = {}

def interpret_block(lines, start_index):
    i = start_index
    while i < len(lines):
        line = lines[i].strip()
        if line == "}":
            return i  # Ende des Blocks
        result = interpret(line, lines, i)
        if result == "inserted":
            i += 1  # eingefügter Code folgt
            continue
        i += 1
    return i

def interpret(line, lines, current_index):
    line = line.strip()

    # Variable setzen
    if line.startswith("set "):
        parts = line[4:-1].split(" = ")
        VarName = parts[0].strip()
        VarValue = eval(parts[1].strip(), {}, variables)
        variables[VarName] = VarValue

    # Benutzereingabe
    elif line.startswith("input (") and line.endswith("\\"):
        content = line[len("input ("):-2].strip()
        parts = content.split(",", 1)
        if len(parts) != 2:
            print("Error: Ungültiges input-Format")
            return
        varname = parts[0].strip()
        frage = parts[1].strip()
        user_input = input(frage + " ")
        try:
            value = eval(user_input, {}, variables)
        except:
            value = user_input
        variables[varname] = value    

    # Ausgabe
    elif line.startswith("write (") and line.endswith(")\\"):
        content = line[7:-2].strip()
        if content.startswith('"') and content.endswith('"'):
            print(content[1:-1])
        elif content in variables:
            print(variables[content])
        else:
            print(f"Error: '{content}' not defined")

    # If-Bedingung
    elif line.startswith("incase "):
        condition = line[7:].strip()
        if condition.endswith("{"):
            condition = condition[:-1].strip()
            try:
                if eval(condition, {}, variables):
                    return "start_block"
                else:
                    return "skip_block"
            except Exception as e:
                print(f"Condition Error: {e}")
                return "skip_block"
    
    # Funktionsdefinition
    elif line.startswith("func "):
        funcName = line[len("func "):].strip()
        if funcName.endswith("{"):
            funcName = funcName[:-1].strip()
        functions[funcName] = []
        return "start_function", funcName

    # Funktionsaufruf
    elif line.startswith("call ") and line.endswith("\\"):
        func_name = line[5:-1].strip()
        if func_name in functions:
            for func_line in functions[func_name]:
                interpret(func_line, lines, current_index)
        else:
            print(f"Error: Funktion '{func_name}' nicht definiert")

    # connect fügt Code ein
    elif line.startswith("connect ") and line.endswith("\\"):
        filepath = line[len('connect src:"'):-2].strip()
        with open(filepath, "r") as file:
            new_lines = file.readlines()
            for l in reversed(new_lines):  # Reihenfolge beibehalten
                lines.insert(current_index + 1, l)

        return "inserted"

    return None


import sys
filename = sys.argv[1]

# Stelle sicher, dass .jal verwendet wird
if not filename.endswith(".jal"):
    filename += ".jal"

with open(filename, "r") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    result = interpret(lines[i], lines, i)

    if result == "inserted":
        i += 1  # weiter mit eingefügter Zeile
    elif isinstance(result, tuple) and result[0] == "start_function":
        func_name = result[1]
        i += 1
        while i < len(lines) and lines[i].strip() != "}":
            functions[func_name].append(lines[i].strip())
            i += 1
        i += 1
    elif result == "start_block":
        i += 1
        i = interpret_block(lines, i)
        i += 1
    elif result == "skip_block":
        i += 1
        while i < len(lines) and lines[i].strip() != "}":
            i += 1
        i += 1
    else:
        i += 1