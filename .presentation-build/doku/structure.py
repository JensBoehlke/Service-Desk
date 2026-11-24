from pathlib import Path

folder = Path(__file__).resolve().parent
parts = (folder/'hauptteil.txt').read_text(encoding='utf-8-sig').strip().split('\n# ')
parts[0] = parts[0][2:]
p = [s.split('\n', 1)[1].strip() for s in parts]

def section(title, text):
    return '# '+title+'\n'+text.strip()

def before(text, marker):
    return text.split(marker,1)[0].strip()

def after(text, marker):
    return text.split(marker,1)[1].strip()

intro = """## 1.1 Projektumfeld
Unser Auftraggeber im Schulprojekt ist die Westfalen Office Solutions GmbH in Dortmund. Laut Aufgabenblatt vertreibt und wartet das Unternehmen Büroausstattung und beschäftigt rund 250 Mitarbeitende. Wir haben ServiceDesk als dreiköpfiges Team im Softwareprojekt DO1 bei der BITLC Business IT Learning Center GmbH bearbeitet.

## 1.2 Projektziel
Wir wollten eine Webanwendung entwickeln, in der Mitarbeitende ihre IT-Probleme erfassen und den Bearbeitungsstand nachsehen können. Der Support erhält eine gemeinsame Arbeitsliste. Die Administration pflegt die Kategorien und die Personen, denen Tickets zugewiesen werden können. Für uns war ein Ticket erst dann sinnvoll, wenn man von der ersten Meldung bis zum Abschluss sehen kann, wo die Bearbeitung gerade steht.

## 1.3 Projektbegründung
"""+p[0].split('\n\n')[0]+"""

## 1.4 Projektschnittstellen
Der Browser ist die Schnittstelle für alle drei Arbeitsbereiche. Die Webanwendung greift über Entity Framework Core auf SQL Server LocalDB zu. Unser gemeinsames GitHub-Repository dient der Zusammenarbeit im Team. Die Ergebnisse stellen wir im Unterricht anhand der Dokumentation und einer Live-Demonstration vor.

## 1.5 Projektabgrenzung
Die Aufgabe sieht Mitarbeitende als Datensätze vor und verlangt keine Anmeldung. Der eingetragene Name dient der Zuordnung der Meldung und wird nicht als Identitätsnachweis verwendet. Die drei Navigationsbereiche stehen für unterschiedliche Aufgaben. Eine Anbindung an das Firmenpostfach oder eine automatische Umwandlung von E-Mails in Tickets ist im Projektumfang nicht vorgesehen.

Die Beschreibung der Implementierung bezieht sich auf den Quellcode vom 20. November 2026, Git-Stand e53a7d7. In Kapitel 6 halten wir fest, welche Prüfungen ausgeführt werden konnten und welche Beobachtungen sich aus der Codeprüfung ergeben.
"""
plan=p[3].replace('3.1 Zeitplan für 13 Unterrichtstage','2.1 Projektphasen und Zeitplan').replace('3.2 Zusammenarbeit und Arbeitsübergaben','2.3 Entwicklungsprozess und Übergaben')
plan=plan.replace('## 2.3',"""## 2.2 Ressourcen und Teamaufteilung
Für die Entwicklung nutzten wir eine Windows-Entwicklungsumgebung mit Visual Studio, .NET 10 und einer lokalen SQL-Datenbank. Ein Browser dient zur Bedienung und für die späteren Tests. Das GitHub-Repository liefert den gemeinsamen Codebestand. Bis zum Einstieg in die MVC-Implementierung haben wir zu dritt gearbeitet. Danach haben wir die technische Verantwortung so verteilt.

@table 0.95 1.73
Teammitglied|Arbeitsbereich ab MVC
Jens Böhlke|Mitarbeiterbereich für Ticketmeldung und Einsicht
Daniel Kowalczyk|Supportbereich für Bearbeitung und Zuweisung
Babak Najafpoursarabi|Adminbereich und SQL-Datenbankanbindung
@end

## 2.3""")
plan=plan.replace('\n\nEin Beispiel für eine Anpassung', '\n\nEin Beispiel für eine Anpassung')
plan=plan.split('\n\nEin Beispiel für eine Anpassung')[0]
analysis=p[1].replace('2.1 Ist Analyse','3.1 Ist-Analyse').replace('2.2 Soll Konzept','3.2 Soll-Konzept')
analysis=analysis.replace('Am Telefon', 'Am Telefon')+"""

Für die Bedienung haben wir uns an einem einfachen Beispiel orientiert. Bei einem nicht erreichbaren Drucker meldet die betroffene Person das Problem mit einem kurzen Titel und einer genaueren Beschreibung. Auf der Supportseite lässt sich der neue Fall über seinen Status finden. Jemand aus dem IT-Team übernimmt ihn und ändert den Bearbeitungsstand. Die meldende Person sieht später in der Ticketliste, ob die IT den Fall abgeschlossen hat.
"""
req = p[2].replace('2.3 Funktionale Anforderungen','3.3 Anwendungsfälle und Anforderungen')
req=before(req,'## 2.4')
uc = after(p[4],'## 3.4 UML Anwendungsfälle')
req = req.replace('wiederzufinden.\n\n@table','wiederzufinden.\n\n'+uc+'\n\n@table')
req += """

## 3.4 Qualitätsanforderungen
Die Navigation soll in jedem Bereich gleich bleiben. Ein ungültiges Formular soll erklären, welches Feld korrigiert werden muss. Aus der Ticketliste sollen Status, Datum und der Weg zu den Details ohne Nachfragen hervorgehen. Die Zuweisung und die Bearbeitung müssen auch nach dem erneuten Aufruf eines Tickets nachvollziehbar sein.
"""
arch=before(p[4],'## 3.4').replace('3.3 Architektur und technische Entscheidungen','4.1 Zielplattform und Architektur')
arch += '\n\n'+after(p[5],'## 3.6 Oberflächenentwurf und Mockups')
mockmarker='Bei den Mockups'
arch=arch.replace(mockmarker,'## 4.2 Oberflächenentwurf und Mockups\n'+mockmarker)
arch=arch.replace('Die Skizzen zeigen die Anordnung der Bedienelemente in vereinfachter Form.','Die Skizzen zeigen die Anordnung der Bedienelemente in vereinfachter Form. Die tannengrüne Navigation und das Westfalen-Logo verbinden die Ansichten optisch.')
data=before(p[5],'## 3.6').replace('3.5 UML Klassendiagramm','4.3 Datenmodell und UML-Klassendiagramm')
data += """

## 4.4 Geschäftsregeln
Eine Meldung aus dem Mitarbeiterbereich beginnt als Offen. Der Support priorisiert sie, vergibt bei Bedarf eine Zuständigkeit und ändert den Bearbeitungsstand. Ein abgeschlossener Fall soll vor einer Inhaltsänderung wieder geöffnet werden. Bei Änderungen an den Stammdaten müssen bestehende Tickets erhalten bleiben. Diese Regeln betreffen mehr als eine Seite und sind deshalb auch Teil der Testplanung.

## 4.5 Qualitätssicherung und Testplanung
"""+before(after(p[6],'## 3.7 Aufbau der Blackboxtests'),'@table')+"""

Wir trennen den Build von der Prüfung im Browser. Ein erfolgreicher Build belegt, dass sich das Projekt übersetzen lässt. Für die Abnahme muss außerdem die Anwendung mit einer erreichbaren SQL-Instanz starten. Die Ist-Spalte in Kapitel 6 hält fest, welche Beobachtungen tatsächlich vorliegen.
"""
jens=p[7].replace('4.1 Jens Böhlke','5.1 Mitarbeiterbereich – Jens Böhlke')
jens=jens.replace('keine passende Action bereitstellt. Das gehört','keine passende Action bereitstellt. Der Bearbeitungsweg gehört in den Support. Die Schaltfläche zählt')
dan=p[8].replace('4.2 Daniel Kowalczyk','5.2 IT-Support – Daniel Kowalczyk')
bab=p[9].replace('4.3 Babak Najafpoursarabi','5.3 Administration – Babak Najafpoursarabi').replace('4.4 Code First und Start der Anwendung','5.4 SQL-Anbindung und Code First – Babak Najafpoursarabi')
integr=p[10].replace('4.5 Vom Modell zum gemeinsamen Ablauf','5.5 Migrationen und gemeinsamer Ablauf').replace('4.6 Gemeinsames Layout und Startseite','5.6 Gemeinsames Layout und Startseite').replace('4.7 Was beim Zusammenführen auffiel','5.7 Erkenntnisse aus der Zusammenführung')
integr=integr.replace('Im Soll-Ist-Vergleich führen wir deshalb','In Kapitel 8 führen wir deshalb')
valid=p[11].replace('Projektregel zur Kategorie anwenden. Ist-Modell erlaubt eine leere Zuordnung.','Im Projektstand wird ein Ticket ohne Kategorie gespeichert.').replace('Kategorie löschen, der ein Testticket zugeordnet ist.','Eine Kategorie mit zugeordnetem Testticket löschen.').replace('IT-Person löschen, der ein Testticket zugewiesen ist.','Eine IT-Person mit zugewiesenem Testticket löschen.')
valid=valid.replace('Die Codebefunde erklären, welche Fälle beim nächsten Lauf besonders wichtig sind. Sie ersetzen keinen beobachteten Blackboxtest.','In einer früheren Projektnotiz ist für das Löschen einer zugewiesenen Person bereits ein SQL-Fremdschlüsselkonflikt protokolliert. Ob die anderen Prüfschritte im aktuellen Build wie vorgesehen ablaufen, bleibt bis zum Browserlauf offen.')
final=p[12].replace('6.1 Soll und Ist im Vergleich','8.1 Soll-Ist-Vergleich').replace('6.2 Reflexion','8.2 Erfahrungen und Teamreflexion').replace('6.3 Fazit und Ausblick','8.3 Ausblick').replace('Jens\\\' Formular','das Formular von Jens')
final=final.replace("Ein Ticket, das Jens' Formular speichert", "Ein Ticket, das das Formular von Jens speichert")
last="""Die Startanleitung im Anhang richtet sich an Personen, die die Anwendung lokal einrichten. Der Bedienablauf im selben Anhang fasst zusammen, wie eine Meldung im Mitarbeiterbereich entsteht und im Support übernommen wird. Unsere technischen Entscheidungen, Testfälle und offenen Punkte haben wir in dieser Projektdokumentation zusammengeführt.

## 8 Fazit
"""+final
items=[
    ('1 Einleitung',intro),('2 Projektplanung',plan),
    ('3 Analysephase',analysis),('3 Analysephase  Fortsetzung',req),
    ('4 Entwurfsphase',arch),('4 Entwurfsphase  Fortsetzung',data),
    ('5 Implementierungsphase',jens),('5 Implementierungsphase  Fortsetzung',dan),
    ('5 Implementierungsphase  Fortsetzung',bab),('5 Implementierungsphase  Fortsetzung',integr),
    ('6 Testphase und Qualitätskontrolle',valid),('7 Dokumentation',last)]
(folder/'document.txt').write_text('\n\n'.join(section(h,t) for h,t in items),encoding='utf-8')
print('Hauptteilseiten:',len(items),'Wörter:',sum(len(t.split()) for _,t in items))

