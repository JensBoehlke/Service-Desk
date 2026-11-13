using Service_Desk.Models;

namespace Service_Desk.Data
{
    // TESTDATEN: Die Initialisierung ist absichtlich einfach und mehrfach ausführbar.
    public static class DatabaseSeeder
    {
        public static void Seed(ServiceDeskContext context)
        {
            // Drei Frauen und drei Männer für die Teamansicht.
            var mitarbeiterNamen = new[]
            {
                "Anna Müller",
                "Lisa Schneider",
                "Sofia Wagner",
                "Daniel Becker",
                "Jonas Hoffmann",
                "Mehmet Kaya"
            };

            foreach (var name in mitarbeiterNamen)
            {
                if (!context.Mitarbeiter.Any(mitarbeiter => mitarbeiter.Name == name))
                {
                    context.Mitarbeiter.Add(new IT_Mitarbeiter { Name = name });
                }
            }

            var kategorieNamen = new[] { "Hardware", "Software", "Netzwerk", "Benutzerkonto" };

            foreach (var name in kategorieNamen)
            {
                if (!context.Kategorie.Any(kategorie => kategorie.KategorieName == name))
                {
                    context.Kategorie.Add(new Kategorie { KategorieName = name });
                }
            }

            context.SaveChanges();

            // Es werden nur in einer leeren Ticket-Tabelle zehn Beispieltickets angelegt.
            if (context.Tickets.Any())
            {
                return;
            }

            var mitarbeiter = context.Mitarbeiter
                .Where(item => mitarbeiterNamen.Contains(item.Name))
                .OrderBy(item => item.MitarbeiterId)
                .ToList();

            var kategorien = context.Kategorie
                .Where(item => kategorieNamen.Contains(item.KategorieName))
                .ToDictionary(item => item.KategorieName);

            var heute = DateTime.Now;

            context.Tickets.AddRange(
                Ticket("Notebook startet nicht", "Das Notebook bleibt beim Startbildschirm hängen.", "Marie König", heute.AddHours(-2), Prioritaet.Hoch, TicketStatus.Offen, kategorien["Hardware"], mitarbeiter[0]),
                Ticket("Passwort zurücksetzen", "Der Zugang zum Intranet ist gesperrt.", "Paul Richter", heute.AddHours(-5), Prioritaet.Mittel, TicketStatus.InBearbeitung, kategorien["Benutzerkonto"], mitarbeiter[3]),
                Ticket("Drucker nicht erreichbar", "Der Drucker im zweiten Stock wird nicht gefunden.", "Nina Schulz", heute.AddDays(-1), Prioritaet.Mittel, TicketStatus.Offen, kategorien["Hardware"], mitarbeiter[1]),
                Ticket("VPN-Verbindung bricht ab", "Die VPN-Verbindung trennt sich nach wenigen Minuten.", "Thomas Klein", heute.AddDays(-1).AddHours(-3), Prioritaet.Hoch, TicketStatus.InBearbeitung, kategorien["Netzwerk"], mitarbeiter[4]),
                Ticket("Office-Update fehlt", "Das aktuelle Office-Update kann nicht installiert werden.", "Laura Neumann", heute.AddDays(-2), Prioritaet.Niedrig, TicketStatus.Abgeschlossen, kategorien["Software"], mitarbeiter[2]),
                Ticket("WLAN im Besprechungsraum", "Im großen Besprechungsraum ist das Signal sehr schwach.", "Felix Braun", heute.AddDays(-2).AddHours(-4), Prioritaet.Mittel, TicketStatus.Offen, kategorien["Netzwerk"], mitarbeiter[5]),
                Ticket("Neue Maus benötigt", "Die linke Maustaste reagiert nur noch gelegentlich.", "Emma Hartmann", heute.AddDays(-3), Prioritaet.Niedrig, TicketStatus.Abgeschlossen, kategorien["Hardware"], mitarbeiter[0]),
                Ticket("Teams-Mikrofon ohne Ton", "In Besprechungen wird kein Mikrofonsignal erkannt.", "Leon Wolf", heute.AddDays(-3).AddHours(-2), Prioritaet.Hoch, TicketStatus.InBearbeitung, kategorien["Software"], mitarbeiter[1]),
                Ticket("Gruppenlaufwerk fehlt", "Das Projektlaufwerk ist im Explorer nicht sichtbar.", "Mia Krüger", heute.AddDays(-4), Prioritaet.Mittel, TicketStatus.Offen, kategorien["Benutzerkonto"], mitarbeiter[3]),
                Ticket("Bildschirm flackert", "Der externe Bildschirm flackert bei hoher Auflösung.", "Noah Peters", heute.AddDays(-5), Prioritaet.Niedrig, TicketStatus.Abgeschlossen, kategorien["Hardware"], mitarbeiter[2])
            );

            context.SaveChanges();
        }

        // TESTDATEN: Kleine Hilfsmethode, damit die Ticketliste gut lesbar bleibt.
        private static Ticket Ticket(
            string titel,
            string beschreibung,
            string erstelltVon,
            DateTime erstelltAm,
            Prioritaet prioritaet,
            TicketStatus status,
            Kategorie kategorie,
            IT_Mitarbeiter mitarbeiter)
        {
            return new Ticket
            {
                Titel = titel,
                Beschreibung = beschreibung,
                ErstelltVon = erstelltVon,
                Erstellungsdatum = erstelltAm,
                Prioritaet = prioritaet,
                Status = status,
                KategorieId = kategorie.KategorieId,
                MitarbeiterId = mitarbeiter.MitarbeiterId
            };
        }
    }
}
