from pathlib import Path
import difflib
import re
import sys

root = Path(sys.argv[1])
patch_path = Path(sys.argv[2])
files = {}


def comment(path, anchor, *lines, after=False):
    path = "Service-Desk/" + path
    before, body, bom = files.get(path, (None, None, None))
    if before is None:
        raw = (root / path).read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        before = body = raw.decode("utf-8-sig").replace("\r\n", "\n")
    starts = list(re.finditer(r"(?m)^([ \t]*)" + re.escape(anchor) + r"[^\n]*\n", body))
    if len(starts) != 1:
        raise ValueError((path, anchor, len(starts)))
    match = starts[0]
    indent = match.group(1)
    if path.endswith(".cshtml"):
        addition = "".join(f"{indent}@* {line} *@\n" for line in lines)
    else:
        addition = "".join(f"{indent}// {line}\n" for line in lines)
    point = match.end() if after else match.start()
    files[path] = (before, body[:point] + addition + body[point:], bom)


comment("Program.cs", "var builder =", "Hier beginnt die Anwendung. Der Builder liest Einstellungen und sammelt die Dienste, die wir gleich brauchen.")
comment("Program.cs", "builder.Services.AddDbContext", "DeskData ist der Name der Verbindungszeichenfolge. Sie sagt EF Core, welchen SQL Server es verwenden soll.",
        "ASP.NET Core erstellt den ServiceDeskContext bei Bedarf und übergibt ihn z. B. an den TicketController.")
comment("Program.cs", "builder.Services.AddControllersWithViews();", "Schaltet MVC ein. Controller nehmen Anfragen an und können Razor-Seiten als Antwort zurückgeben.")
comment("Program.cs", "app.MapStaticAssets();", "Statische Dateien sind z. B. CSS und Bilder. Die Route darunter ordnet URLs den Controller-Methoden zu.",
        "Beispiel: /Support/Details/5 ruft Details im SupportController mit id = 5 auf. / führt zu Home/Index.")
comment("Program.cs", "using (var scope", "Vor dem Start des Webservers: Kontext holen, fehlende Änderungen am Datenbankschema anwenden und Demodaten vorbereiten.")

comment("Models/ServiceDeskContext.cs", "public class ServiceDeskContext", "Der DbContext ist unsere Verbindung zwischen C#-Objekten und den Tabellen in SQL Server.",
        "Über ein DbSet lesen wir Datensätze. Änderungen werden erst mit SaveChanges oder SaveChangesAsync in die Datenbank geschrieben.")
comment("Models/Ticket.cs", "[Key]", "Die TicketId ist der Primärschlüssel. Damit lässt sich jedes Ticket eindeutig finden.")
comment("Models/Ticket.cs", '[Required(ErrorMessage = "Bitte Ihre', "ErstelltVon ist der eingegebene Name der meldenden Person. Er verweist auf keinen Mitarbeiterdatensatz.",
        "Required verlangt eine Eingabe, StringLength begrenzt ihre Länge und Display bestimmt die sichtbare Feldbezeichnung.")
comment("Models/Ticket.cs", "public DateTime Erstellungsdatum", "Der Initialwert wird gesetzt, wenn C# ein neues Ticket-Objekt erzeugt. Der Support setzt das Datum beim Speichern ausdrücklich neu.")
comment("Models/Ticket.cs", "public Prioritaet Prioritaet", "Die Enums legen die gültigen Werte für Dringlichkeit und Bearbeitungsstand fest. Hier stehen die Startwerte.")
comment("Models/Ticket.cs", '[Display(Name = "Bearbeiter")]', "MitarbeiterId ist der Fremdschlüssel. int? erlaubt null, solange niemand zugewiesen ist.",
        "Mitarbeiter ist das dazugehörige Objekt. Damit kann die Ansicht z. B. den Namen anzeigen, wenn der Controller es mit Include lädt.")
comment("Models/Ticket.cs", '[Display(Name = "Kategorie")]', "Auch die Kategorie ist optional. KategorieId speichert die Verknüpfung, Kategorie steht für das zugehörige Objekt.")
comment("Models/IT_Mitarbeiter.cs", "public ICollection<Ticket> Tickets", "Ein IT-Mitarbeiter kann mehrere Tickets übernehmen. Die Liste bildet die Rückrichtung zur MitarbeiterId im Ticket ab.")
comment("Models/Kategorie.cs", "public ICollection<Ticket> Tickets", "Eine Kategorie kann für mehrere Tickets verwendet werden. Jedes Ticket hat höchstens eine Kategorie.")

ticket = "Controllers/TicketController.cs"
comment(ticket, "public class TicketController", "Mitarbeiterbereich: Tickets melden, in der Übersicht ansehen und ihre Details aufrufen.")
comment(ticket, "public TicketController(", "ASP.NET Core liefert den Datenbankkontext, der in Program.cs registriert wurde.")
comment(ticket, "var tickets = await _context.Tickets", "Include lädt das verknüpfte Kategorie-Objekt mit. ToListAsync führt die Abfrage aus und liefert eine Liste.")
comment(ticket, "if (Enum.TryParse", "Der Filter kommt als Text aus der URL. Wir wenden ihn erst nach dem Laden auf die Liste an.")
comment(ticket, "public async Task<IActionResult> Details(int? id)", "Details sucht das Ticket anhand seiner ID. Fehlt die ID oder das Ticket, antwortet der Server mit HTTP 404.")
comment(ticket, "public async Task<IActionResult> Create()", "GET zeigt das leere Formular. Das Dropdown zeigt die Namen der Kategorien und sendet beim Absenden ihre ID.")
comment(ticket, "public async Task<IActionResult> Create([Bind", "POST erhält das abgeschickte Formular. Bind bestimmt, welche Eigenschaften ASP.NET Core aus der Anfrage übernehmen darf.")
comment(ticket, "[ValidateAntiForgeryToken]", "ASP.NET Core prüft die Kennung aus dem Formular. Das schützt davor, dass eine fremde Seite das Formular im Namen des Nutzers abschickt.")
comment(ticket, "if (ModelState.IsValid)", "ModelState enthält Eingabe- und Prüffehler. Bei Fehlern zeigt View(ticket) das ausgefüllte Formular erneut.",
        "Die Kategorien werden vorher erneut bereitgestellt, damit auch das Dropdown seine Auswahl behält.")
comment(ticket, "_context.Add(ticket);", "Add merkt das neue Ticket zur Speicherung vor. SaveChangesAsync schreibt es tatsächlich in die Datenbank.")

support = "Controllers/SupportController.cs"
comment(support, "public class SupportController", "IT-Support: Tickets filtern, zuweisen, bearbeiten, wieder öffnen und löschen.")
comment(support, "var tickets = _context.Tickets", "Hier entsteht eine Datenbankabfrage. Include lädt Bearbeiter und Kategorie mit.",
        "Jeder gewählte Filter hängt eine Bedingung an. Erst ToListAsync führt die kombinierte Abfrage aus.")
comment(support, "return View(await tickets", "Der Controller gibt die gefundenen Tickets als Model an Views/Support/Index.cshtml weiter.")
comment(support, "public async Task<IActionResult> Create()", "GET öffnet das Formular und füllt seine Auswahllisten aus den Stammdaten.")
comment(support, '[Bind("ErstelltVon,Titel', "POST nimmt die hier angegebenen Felder aus dem Formular entgegen. Das Erstellungsdatum setzt der Server.")
comment(support, "public async Task<IActionResult> Edit(int? id)", "GET lädt das gespeicherte Ticket samt aktueller Auswahl. Die Methode zeigt das Formular an.")
comment(support, "public async Task<IActionResult> Edit(int id)", "POST lädt das vorhandene Ticket erneut. TryUpdateModelAsync übernimmt und prüft nur die unten aufgeführten Felder.")
comment(support, "catch (DbUpdateConcurrencyException)", "Wenn EF Core beim Speichern einen Konflikt meldet, prüfen wir, ob das Ticket noch existiert.",
        "Ist er inzwischen gelöscht, folgt HTTP 404. Andere Konflikte gehen an die Fehlerbehandlung weiter.")
comment(support, "public async Task<IActionResult> Reopen(", "Wiederöffnen ist ein eigener Formularschritt. Wir setzen den Status auf Offen, speichern und kehren zur Übersicht zurück.")
comment(support, "public async Task<IActionResult> Delete(int? id)", "GET zeigt die Rückfrage mit den Ticketdaten. Erst die POST-Methode DeleteConfirmed führt das Löschen aus.")
comment(support, "private async Task PopulateMitarbeiterDropDownListAsync", "Die SelectList enthält die ID als Formularwert und den Namen als Anzeigetext. selectedMitarbeiterId markiert die bisherige Auswahl.")
comment(support, "private async Task PopulateKategorieDropDownListAsync", "Dasselbe Prinzip für Kategorien: Name anzeigen, ID senden und die vorige Auswahl bei Bedarf wieder anzeigen.")

staff = "Controllers/IT_MitarbeiterController.cs"
category = "Controllers/KategorieController.cs"
comment(staff, "ViewBag.Kategorien =", "Der Adminbereich zeigt zwei Listen. Die Mitarbeiterliste ist das Model, die Kategorien kommen zusätzlich über ViewBag.")
comment(category, 'return RedirectToAction("Index", "IT_Mitarbeiter");', "Die Kategorien werden auf der gemeinsamen Adminseite gepflegt. Deshalb führt diese Adresse dorthin weiter.")
for path, key, name in ((staff, "mitarbeiterid", "IT-Mitarbeiter"), (category, "kategorieid", "Kategorie")):
    comment(path, "public IActionResult Create()", f"GET zeigt das leere Formular für den neuen Datensatz ({name}).")
    comment(path, "public async Task<IActionResult> Create([Bind", "POST empfängt die Felder aus dem Formular. Bei ungültigen Eingaben erscheint es erneut mit den Fehlermeldungen.")
    comment(path, f"public async Task<IActionResult> Edit(int? {key})", "GET lädt die vorhandenen Werte, damit das Bearbeitungsformular sie anzeigen kann.")
    comment(path, f"public async Task<IActionResult> Edit(int? {key},", "POST vergleicht die ID aus der Anfrage mit der ID des Formularmodells. Bei gültigen Eingaben speichert EF Core die Änderungen.")
    comment(path, f"public async Task<IActionResult> Delete(int? {key})", "GET lädt den Datensatz für die Löschbestätigung. Die Datenbank wird erst beim Absenden geändert.")
comment(staff, "_context.Mitarbeiter.Remove(it_mitarbeiter);", "EF Core merkt die Person zum Löschen vor. Diese Methode löst vorhandene Ticketzuweisungen vorher nicht auf.")
comment(category, "var tickets = await _context.Tickets", "Vor dem Löschen holen wir alle betroffenen Tickets. Ihre KategorieId wird geleert, damit die Tickets erhalten bleiben.")
comment(category, "_context.Kategorie.Remove(kategorie);", "SaveChangesAsync speichert die gelösten Zuordnungen und das Löschen der Kategorie gemeinsam.")
comment("Controllers/HomeController.cs", "public IActionResult Index()", "Die Standardroute aus Program.cs landet hier. View() verwendet die Startseite Views/Home/Index.cshtml.")

comment("Data/DatabaseSeeder.cs", "public static void Seed(", "Füllt die Datenbank für Demo und Tests mit Beispielwerten, wenn die benötigten Daten fehlen.")
comment("Data/DatabaseSeeder.cs", "if (context.Tickets.Any())", "Sobald Tickets vorhanden sind, wird die Liste der Beispieltickets übersprungen. So kommen diese nicht bei jedem Neustart erneut dazu.")
comment("Data/DatabaseSeeder.cs", "context.Tickets.AddRange(", "AddRange merkt alle Beispieltickets auf einmal zum Einfügen vor. SaveChanges speichert sie anschließend.")

comment("Views/Ticket/Index.cshtml", "@model", "Model ist die Ticketliste aus TicketController.Index. Die Schleife weiter unten erzeugt für jedes Ticket eine Tabellenzeile.", after=True)
comment("Views/Ticket/Create.cshtml", '<form asp-controller="Ticket"', "Das Formular sendet per POST an TicketController.Create. asp-for verknüpft Eingaben mit den Eigenschaften des Tickets.",
        "asp-validation-for zeigt die Meldung zum jeweiligen Feld an, wenn die Eingabe nicht passt.")
comment("Views/Ticket/Details.cshtml", "@model", "Diese Seite zeigt ein einzelnes Ticket. Model.Titel greift auf den Titel dieses Tickets zu.", after=True)
comment("Views/Support/Index.cshtml", "@inject", "Model liefert die gefilterten Tickets für die Liste. Database wird zusätzlich für die Kennzahlen über alle Tickets verwendet.", after=True)
comment("Views/Support/Index.cshtml", '<form method="get"', "Ein GET-Formular schreibt die gewählten Filter in die URL. Der Controller verwendet diese Werte beim Laden der Tickets.")
comment("Views/Support/Edit.cshtml", '<form asp-action="Edit"', "asp-route-id setzt die ID in die Formularadresse. Beim Absenden weiß der Controller so, welches Ticket geändert werden soll.")
comment("Views/Support/Create.cshtml", '<form asp-action="Create"', "Der Support darf im Formular zusätzlich den Startstatus und die zuständige Person auswählen.")
comment("Views/Support/Delete.cshtml", '<form asp-action="Delete"', "Erst diese Bestätigung sendet den POST zum Löschen. Die ID identifiziert das betreffende Ticket.")
comment("Views/IT_Mitarbeiter/Index.cshtml", "@inject", "Die Seite bekommt die Personenliste als Model und die Kategorien über ViewBag. Die Ticketzahlen werden zusätzlich aus der Datenbank gelesen.", after=True)
comment("Views/Shared/_Layout.cshtml", "@RenderBody()", "Hier setzt Razor den Inhalt der aktuellen Seite ein. Die gemeinsame Navigation steht außen herum im Layout.")

patch = []
count = 0
for path, (before, after, bom) in sorted(files.items()):
    original = ("\ufeff" if bom else "") + before
    updated = ("\ufeff" if bom else "") + after
    diff = list(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), f"a/{path}", f"b/{path}"))
    changes = [line[1:].strip() for line in diff[2:] if line.startswith("+")]
    assert not any(line.startswith("-") for line in diff[2:]), path
    assert all(line.startswith("//") or (line.startswith("@*") and line.endswith("*@")) for line in changes), path
    count += len(changes)
    patch.append(f"diff --git a/{path} b/{path}\n")
    patch.extend(diff)
patch_path.write_text("".join(patch), encoding="utf-8", newline="\n")
print(f"{len(files)} Dateien, {count} Kommentarzeilen")
