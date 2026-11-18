# Service-Desk · Übergabe vom 18.11.2026

- **Arbeitsordner:** `C:\Users\DanielKowalczyk\source\repos\Service-Desk`. Der Stand aus `Desktop\Service-Desk3` wurde ins Original übernommen. Solution: `Service-Desk.slnx` (ASP.NET Core MVC, .NET 10).
- **Git:** Aktiver Branch ist `master`. Beim Schreiben liegen die Änderungen noch lokal und sind nicht committet. Vor dem nächsten Commit `git status` prüfen. Zusätzlich liegen die HTML- und PDF-Doku zur Übernahme im Repo-Ordner.
- **Startseite:** In `Service-Desk/Views/Home/Index.cshtml` stehen Logo links und „Westfalen Office / Solutions GmbH“ zweizeilig rechts daneben, zusammen oben mittig. Darunter steht groß „SERVICE-DESK“.
- **Schriftzug:** In `Service-Desk/wwwroot/css/site.css` unter `.home-service-desk-label` stehen Schriftgröße, Buchstabenabstand (`.28em`) und vertikale Stauchung (`scaleY(.7)`). Bei „gestaucht“ ist hier die Höhe gemeint.
- **Logo und Navi:** `Service-Desk/wwwroot/images/westfalen-logo.png` enthält die tannengrüne Westfalen-Karte (`#102b20`) mit transparentem Außenbereich. Startseite und Navi nutzen dieselbe Datei. Die dünne weiße Kartenkontur entsteht in der Navi per CSS unter `.app-sidebar .company-logo`.
- **Seiten und Zuständigkeit:** Die Navi steht in `Service-Desk/Views/Shared/_Layout.cshtml`. Startseite → `Home/Index`, Mitarbeiter → `Ticket/Index`, Support → `Support/Index`, Admin-Bereich → `IT_Mitarbeiter/Index`. Im Mitarbeiterbereich gibt es „Details“ und kein „Bearbeiten“. Die Bearbeitung gehört in den Support.
- **Geprüft:** `dotnet build Service-Desk.slnx --no-restore` lief nach Einbau des Startseiten-Schriftzugs mit 0 Fehlern und 0 Warnungen. Danach kamen die vertikale Stauchung und weiße Kontur als reine CSS-Änderungen hinzu.
