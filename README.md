# Python Passwort-Manager

Dies ist ein einfacher Passwort-Manager, der mit Python und Tkinter entwickelt wurde. Der Manager ermöglicht es Benutzern, sich zu registrieren, anzumelden und verschlüsselte Passwörter sicher zu speichern. Die Daten werden in einer SQLite-Datenbank gespeichert, und Passwörter werden mit dem **Fernet**-Verschlüsselungssystem gesichert.

## Funktionen

- **Registrierung**: Neue Benutzer können ein Konto erstellen und ihre Passwörter sicher speichern.
- **Anmeldung**: Bestehende Benutzer können sich anmelden und auf ihre gespeicherten Passwörter zugreifen.
- **Passwortverschlüsselung**: Passwörter werden mit dem **Fernet**-Verschlüsselungsstandard gesichert.
- **Passwortverwaltung**: Benutzer können neue Passwörter hinzufügen, anzeigen und die Details jedes gespeicherten Passworts einsehen.
- **Logout**: Benutzer können sich abmelden und zur Anmeldeseite zurückkehren.

## Abhängigkeiten

- `tkinter`: Zum Erstellen der grafischen Benutzeroberfläche (GUI).
- `cryptography`: Für die Passwortverschlüsselung mit **Fernet**.
- `sqlite3`: Für die Speicherung von Benutzern und Passwörtern in einer lokalen SQLite-Datenbank.

Installiere die notwendigen Python-Pakete mit:

```bash
pip install cryptography
pip install tkinter
pip install sqlite3
```
## Projekt builden

```bash
git clone https://github.com/besimshala03/passwordmanager.git
python main.py

```

## Verwendung
1. Registrierung: Beim ersten Start des Programms klicke auf "Register", um ein neues Konto zu erstellen. Gib deinen Benutzernamen und dein Passwort ein.
2. Anmeldung: Nach der Registrierung kannst du dich mit deinen Anmeldeinformationen einloggen.
3. Passwort hinzufügen: Nach dem Login kannst du ein neues Passwort mit einem zugehörigen Benutzernamen und einer URL hinzufügen.
4. Passwörter anzeigen: Du kannst deine gespeicherten Passwörter einsehen und auf Details zugreifen, indem du auf den Benutzernamen klickst.
5. Logout: Über die Schaltfläche "Logout" kannst du dich abmelden.

## Sicherheit
- Passwörter werden vor der Speicherung mithilfe des Fernet-Verschlüsselungsverfahrens verschlüsselt.
- Benutzerkennwörter werden mit dem SHA-256-Algorithmus gehasht, um zusätzliche Sicherheit zu gewährleisten.

# Datenbankstruktur
- users: Speichert Benutzernamen, gehashte Passwörter und Benutzer-IDs.
- keys: Speichert Benutzer-IDs und Verschlüsselungsschlüssel für jeden Benutzer.
- passwords: Speichert verschlüsselte Passwörter, zugehörige URLs und Benutzernamen.

