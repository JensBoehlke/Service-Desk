# Service Desk

Ein einfacher Service-Desk- bzw. Helpdesk-Workflow, aufgebaut als ASP.NET Core Webanwendung auf .NET 10.

## Überblick

Dieses Projekt dient als Grundlage für eine interne Service-Desk-Anwendung zur Verwaltung von Anfragen, Tickets und Supportprozessen. Der aktuelle Stand ist ein Basisprojekt mit dem Standard-Setup für ASP.NET Core MVC.

## Technologien

- .NET 10
- ASP.NET Core MVC
- Razor Views / MVC-Pattern
- C#
- GitHub für Kollaboration

## Voraussetzungen

Vor dem Start benötigst du:

- .NET 10 SDK
- Visual Studio 2026 oder ein anderer .NET-Entwicklungs-Editor
- Git

## Projekt lokal starten

1. Repository klonen:
   ```bash
   git clone https://github.com/JensBoehlke/Service-Desk.git
   cd Service-Desk
   ```

2. Abhängigkeiten wiederherstellen:
   ```bash
   dotnet restore
   ```

3. Anwendung starten:
   ```bash
   dotnet run
   ```

4. Die Anwendung öffnest du anschließend im Browser unter:
   ```text
   https://localhost:5001
   ```
   bzw. je nach Konfiguration:
   ```text
   http://localhost:5000
   ```

## Build

Zum Bauen des Projekts:

```bash
dotnet build
```

## Projektstruktur

```text
Service-Desk/
├── Service-Desk.slnx
├── Service-Desk/
│   ├── Program.cs
│   ├── Service-Desk.csproj
│   ├── Controllers/
│   ├── Models/
│   ├── Views/
│   └── wwwroot/
├── README.md
└── .gitignore
```

## Status

Das Projekt befindet sich aktuell im Initial-Setup / Basis-Framework-Status. Je nach Entwicklungsstand können später weitere Funktionen ergänzt werden, z. B.:

- Ticket-Erstellung
- Statusverwaltung
- Prioritäten und Zuweisungen
- Benutzerauthentifizierung
- Dashboard für Support-Anfragen
- Reporting und Export

## Beitrag

Beiträge sind willkommen. Bitte arbeite dabei idealerweise in einem eigenen Branch:

```bash
git checkout -b feature/deine-aenderung
```

Danach Änderungen committen und über GitHub ein Pull Request erstellen.

## Lizenz

Dieser Projektstand ist aktuell ohne explizite Open-Source-Lizenz hinterlegt. Bitte vor der öffentlichen Nutzung oder Verteilung die Lizenzbedingungen prüfen.

## Hinweise

Das Repository ist für die gemeinsame Entwicklung vorbereitet. Für eine strukturierte Teamarbeit empfiehlt sich:

- eigener Branch pro Feature
- kurze, verständliche Commits
- regelmäßiges Pulling vor dem Push
- Review durch andere Teammitglieder vor dem Merge
