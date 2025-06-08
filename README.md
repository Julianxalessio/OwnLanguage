# Mini-Interpreter

Ein einfacher Interpreter für eine selbst definierte Miniprogrammiersprache.  
Er unterstützt Variablen, Ausgaben und einfache Bedingungsblöcke (`incase`).

## 🔧 Funktionen

- `set <VariableName> = <VariableValue>\` – legt eine Variable an
- `write (<VariableName>)\` – gibt eine Variable aus
- `write (*<String>*)\` – gibt einen Text aus
- `incase <Bedingung> { ... }` – führt einen Block nur aus, wenn die Bedingung wahr ist
- `input (<VariableName>, <Question>)\` - fragt den User nach einer Eingabe
- `func <Funktionsname> { ... }` - erstellt eine Funktion
- `call <Funktionsname>\` - ruft eine bereits erstellte Funktion auf
- `connect src:"<FilePath>"\` - ermöglicht es nachfolgend des Connectcodes den Code aus dem verknüpften File einzufügen

## Run Interpretrer

- `python interpreter.py`

## Files

- `run.py` - Der Interpreter
- `NameDerDatei.jal` - Das Codefile

Es könne noch mehr von den Code-Files erstellt werden, diese müssen dann aber in run.py hinzugefügt werden.

## Develepor

Julian Alessio Lombardo