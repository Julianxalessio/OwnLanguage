import * as vscode from 'vscode';
import * as path from 'path';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('mylanguage.run', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('Kein aktiver Editor!');
            return;
        }

        const doc = editor.document;
        const filepath = doc.fileName;

        if (!filepath.endsWith('.mini')) {
            vscode.window.showErrorMessage('Nur .mini-Dateien werden unterstützt.');
            return;
        }

        const runScript = path.join(context.extensionPath, 'run.py');

        const terminal = vscode.window.createTerminal('MyLanguage Runner');
        terminal.show();
        terminal.sendText(`python "${runScript}" "${filepath}"`);
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
