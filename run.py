variables = {}
functions = {}

def interpret_block(lines, start_index):
    i = start_index
    while i < len(lines):
        line = lines[i].strip()
        if line == "}":
            return i  # Ende des Blocks
        interpret(line)
        i += 1
    return i

def interpret(line):
    line = line.strip()

    #Variable setzen
    if line.startswith("set "):
        parts = line[4:-1].split(" = ")
        VarName = parts[0].strip()
        VarValue = eval(parts[1].strip(), {}, variables)
        variables[VarName] = VarValue

    elif line.startswith("input (") and line.endswith("\\"):
        content = line[len("input ("):-2].strip()  # Nur 1 Zeichen abschneiden!

        # Zerlege anhand von Komma
        parts = content.split(",", 1)
        if len(parts) != 2:
            print("Error: Ungültiges input-Format")
            return

        varname = parts[0].strip()
        frage = parts[1].strip()

        # Benutzer nach Eingabe fragen
        user_input = input(frage + " ")
        try:
            value = eval(user_input, {}, variables)
        except:
            value = user_input  # Wenn keine Zahl oder Ausdruck, dann als String

        variables[varname] = value    

    elif line.startswith("write (") and line.endswith(")\\"):
        content = line[7:-2].strip()
        #löscht write ( )\
        if content.startswith("*") and content.endswith("*"):
            #löscht **
            print(content[1:-1])
        elif content in variables:
            print(variables[content])
        else:
            print(f"Error: '{content}' not defined")

    # if-Anweisung (incase)
    elif line.startswith("incase "):
        condition = line[7:].strip()
        if condition.endswith("{"):
            condition = condition[:-1].strip()
            try:
                if eval(condition, {}, variables):
                    return "start_block"  # Signalisiere, dass Block folgt
                else:
                    return "skip_block"
            except Exception as e:
                print(f"Condition Error: {e}")
                return "skip_block"
    
    elif line.startswith("func "):
        funcName = line[len("func "):].strip()
        if funcName.endswith("{"):
            funcName = funcName[:-1].strip()
        functions[funcName] = []
        return "start_function", funcName
    
    elif line.startswith("call ") and line.endswith("\\"):
        func_name = line[5:-1].strip()
        if func_name in functions:
            for func_line in functions[func_name]:
                interpret(func_line)
        else:
            print(f"Error: Funktion '{func_name}' nicht definiert")


import sys
filename = sys.argv[1]

with open(filename, "r") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    result = interpret(lines[i])
    if isinstance(result, tuple) and result[0] == "start_function":
        func_name = result[1]
        i += 1
        while i < len(lines) and lines[i].strip() != "}":
            functions[func_name].append(lines[i].strip())
            i += 1
    elif result == "start_block":
        i += 1
        i = interpret_block(lines, i)
    elif result == "skip_block":
        i += 1
        while i < len(lines) and lines[i].strip() != "}":
            i += 1
    i += 1
