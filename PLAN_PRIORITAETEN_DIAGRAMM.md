# Plan: Prioritäten-Diagramm

## Aktueller Stand

Noch keine Umsetzung im Anwendungscode. Dieses Dokument sammelt zunächst nur die gemeinsam abgestimmten Anforderungen.

## Gewünschte Darstellung

Auf der Support-Seite soll ein gestapeltes horizontales Balkendiagramm entstehen, orientiert am bereitgestellten Beispielbild.

Das Diagramm enthält drei horizontale Balken:

1. **Offen** – Prioritätsverteilung aller offenen Tickets
2. **In Bearbeitung** – Prioritätsverteilung aller Tickets in Bearbeitung
3. **Alle Tickets** – Prioritätsverteilung über sämtliche Tickets, einschließlich abgeschlossener Tickets

Jeder Balken wird in drei Abschnitte nach Priorität unterteilt:

- **Grün:** niedrige Priorität
- **Gelb:** mittlere Priorität
- **Rot:** hohe Priorität

Die Farben sollen bewusst wie eine Ampel funktionieren: Grün – Gelb – Rot.

## Schematische Darstellung

```text
Offen           [ Niedrig |      Mittel      | Hoch ]
In Bearbeitung  [ Niedrig | Mittel |      Hoch       ]
Alle Tickets    [    Niedrig    | Mittel |    Hoch   ]
```

## Ebenfalls gewünschte Layoutänderung

- Die vorhandenen Felder **Offen**, **In Bearbeitung** und **Abgeschlossen** sollen kleiner werden.
- Diese drei Statusfelder sollen links angeordnet werden.
- Das Prioritäten-Diagramm soll daneben erscheinen.

## Vorgehensweise

- Änderungen werden gemeinsam Schritt für Schritt geplant.
- Vor jedem Eingriff in den Anwendungscode wird der nächste Schritt erklärt und abgestimmt.
- Es wird nichts ohne ausdrückliches „Weiter“ umgesetzt.

## Noch gemeinsam zu entscheiden

- Genaue Größe und Anordnung der drei Statusfelder
- Genaue Breite und Höhe des Diagramms
- Zahlen direkt in den Balken, daneben oder nur über eine Legende
- Umsetzung mit reinem HTML/CSS oder mit einer Diagrammbibliothek
- Verhalten auf kleinen Bildschirmen
