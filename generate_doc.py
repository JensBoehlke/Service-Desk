import os
import zipfile
from xml.sax.saxutils import escape

out = r'C:\Users\J_B\source\repos\Service-Desk\GitHub-Visual-Studio-Branch-Teamarbeit-Anleitung.docx'

paragraphs = [
	'Arbeitsanleitung: Drei Personen gemeinsam an einem GitHub-Branch in Visual Studio',
	'',
	'Ziel',
	'Mit drei Personen auf demselben GitHub-Branch zusammenzuarbeiten, ohne den Haupt-Branch zu beschädigen. Der Workflow ist für kleine Teams geeignet, wenn alle auf dieselbe Feature-Entwicklung oder denselben Fix hinarbeiten.',
	'',
	'Voraussetzungen',
	'- Zugriff auf das GitHub-Repository mit Schreibrechten',
	'- Alle drei Personen sind als Collaborator im Repository eingetragen',
	'- Visual Studio 2022/2026 mit GitHub-Unterstützung installiert',
	'- Git für Windows ist installiert und in Visual Studio konfiguriert',
	'- Jeder hat den Repository-Clone lokal auf dem Rechner',
	'',
	'1. Shared Branch anlegen',
	'1. Auf GitHub im Repository auf „Branches“ gehen.',
	'2. Einen neuen Branch anlegen, z. B. feature/mehrere-mitarbeiter-teamarbeit oder bugfix/shared-branch.',
	'3. Den Branch direkt aus der Hauptentwicklung bzw. aus main erstellen.',
	'4. Den Branch im Team als gemeinsamen Arbeitszweig nutzen.',
	'',
	'2. Teammitglieder einladen',
	'1. In GitHub auf „Settings“ > „Collaborators“ gehen.',
	'2. Die drei Personen als Collaborator hinzufügen, falls noch nicht geschehen.',
	'3. Sicherstellen, dass alle die richtige Berechtigung haben: mindestens „Write“ oder „Maintain“.',
	'',
	'3. Branch in Visual Studio öffnen',
	'1. Visual Studio starten.',
	'2. „Git“ > „Repository öffnen“ oder „Klonen“ wählen und das Repository auswählen.',
	'3. Den gemeinsamen Branch über „Git-Branches“ oder „Branches“ auswählen und auschecken.',
	'4. Wenn der Branch noch nicht lokal vorhanden ist, mit „Fetch“ oder „Pull“ synchronisieren und danach auschecken.',
	'',
	'4. Vor dem Arbeiten immer aktualisieren',
	'Wichtige Regel: Bevor du mit einer neuen Änderung beginnst, ziehst du zuerst den aktuellen Stand des Branches. So vermeidest du Überschreibungen und Konflikte.',
	'In Visual Studio:',
	'- Git-Status prüfen',
	'- „Fetch“ oder „Pull“ ausführen',
	'- Wenn Änderungen anderer vorhanden sind, diese zuerst übernehmen',
	'',
	'5. Gemeinsam arbeiten auf einem Branch',
	'1. Jede Person arbeitet im selben Branch, nicht in getrennten Spezial-Branches.',
	'2. Vor dem Commit: immer den neuesten Stand ziehen.',
	'3. Kleine, klare Commits machen, z. B. „UI: Formular angepasst“, „API: Fehlerbehandlung ergänzt“.',
	'4. Nach jedem Commit mit „Push“ den Stand ins GitHub-Repository senden.',
	'5. Jeder arbeitet an einem klar abgegrenzten Teil, damit Überschneidungen minimiert werden.',
	'',
	'6. Konflikte vermeiden',
	'Konflikte entstehen, wenn zwei Personen dieselbe Stelle in derselben Datei bearbeiten. Das ist normal. So gehst du vor:',
	'- Vor dem Arbeiten aktuell ziehen',
	'- In derselben Datei nur die eigenen Abschnitte ändern',
	'- Häufig pushen und pullen',
	'- Wenn ein Konflikt entsteht: „Git Changes“ > „Conflicts“ öffnen',
	'- In Visual Studio die Konfliktstellen vergleichen und entscheiden',
	'- Nach dem Auflösen den Konflikt als „Resolved“ markieren und Commit + Push',
	'',
	'7. Wie ein Commit in Visual Studio erstellt wird',
	'1. Änderungen im Projekt ansehen.',
	'2. In der Git-Ansicht die gewünschten Dateien auswählen.',
	'3. Commit-Nachricht schreiben, z. B. „Add: Teamarbeits-Workflow ergänzt“.',
	'4. Auf „Commit All“ oder „Commit Selected“ klicken.',
	'5. Danach „Push“ wählen.',
	'',
	'8. Wie man einen gemeinsamen Stand synchronisiert',
	'1. In Visual Studio auf „Git“ oder „Synchronisieren“ gehen.',
	'2. „Pull“ ausführen, damit alle Änderungen des Teams geladen werden.',
	'3. Wenn der Pull Konflikte zeigt, diese auflösen.',
	'4. Nach der Lösung erneut Commit und Push durchführen.',
	'',
	'9. Pull Request und Freigabe',
	'Wenn der gemeinsame Branch fertig ist:',
	'1. Auf GitHub auf den Branch gehen.',
	'2. „Compare & pull request“ wählen.',
	'3. Den Pull Request für main oder den Ziel-Branch erstellen.',
	'4. Die Teammitglieder als Reviewer hinzufügen.',
	'5. Änderungen prüfen, kommentieren und ggf. Anmerkungen einbauen.',
	'6. Nach Freigabe den Pull Request zusammenführen (Merge).',
	'',
	'10. Gute Teamregeln für drei Personen',
	'- Nur ein gemeinsamer Branch für die Aufgabe',
	'- Vor dem Start immer pullen',
	'- Kleine Commits, keine riesigen Änderungen',
	'- Keine ungetesteten Änderungen direkt in den Zielbranch mergen',
	'- Pull Requests nicht ignorieren',
	'- Vor dem Merge die Funktion auf dem Branch testen',
	'',
	'11. Empfohlene Vorgehensweise in der Praxis',
	'Beispiel:',
	'1. Person A startet den gemeinsamen Branch.',
	'2. Person B und C klonen oder checken den Branch aus.',
	'3. Jeder bearbeitet einen klaren Bereich, z. B. UI, Datenmodell oder Tests.',
	'4. Alle 1–2 Stunden wird gepusht bzw. synchronisiert.',
	'5. Konflikte werden sofort aufgelöst, statt sie aufzuschieben.',
	'6. Wenn die Funktion fertig ist, wird ein Pull Request erstellt und gemeinsam geprüft.',
	'',
	'12. Wichtige Hinweise',
	'- Ein gemeinsamer Branch ist praktisch, aber nur für eine definierte Aufgabe geeignet.',
	'- Wenn mehrere Teams gleichzeitig parallel arbeiten, besser mehrere Feature-Branches verwenden.',
	'- Branch-Protection-Regeln auf GitHub empfehlen, damit der main-Branch nicht direkt ohne Review geändert wird.',
	'- Teamkommunikation ist entscheidend: Wer arbeitet an welcher Datei?',
	'',
	'13. Kurzfassung',
	'1. Branch auf GitHub erstellen',
	'2. Teammitglieder als Collaborator einladen',
	'3. Branch in Visual Studio öffnen',
	'4. Vor dem Arbeiten pullen',
	'5. Commit + Push im gemeinsamen Branch',
	'6. Konflikte sofort lösen',
	'7. Pull Request erstellen und freigeben',
	'8. Nach Review den Branch in main mergen',
	'',
	'Hinweis',
	'Wenn mehrere Personen gleichzeitig dieselbe Datei bearbeiten, ist eine klare Aufteilung der Bereiche oder eine feste Arbeitsreihenfolge wichtig. So bleibt der gemeinsame Branch stabil und das Arbeiten effizient.',
	'',
	'Diese Anleitung ist als praxisnahe Vorgehensweise für kleine Teams gedacht und kann je nach Projektstruktur leicht angepasst werden.'
]

# minimal DOCX package
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
	z.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>''')
	z.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''')
	z.writestr('docProps/core.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>GitHub Branch Teamarbeit in Visual Studio</dc:title>
  <dc:creator>GitHub Copilot</dc:creator>
  <cp:lastModifiedBy>GitHub Copilot</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-11-10T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-10T00:00:00Z</dcterms:modified>
</cp:coreProperties>''')
	z.writestr('docProps/app.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>''')

	body = '\n'.join(
		f'<w:p><w:r><w:t>{escape(p)}</w:t></w:r></w:p>' if p else '<w:p/>'
		for p in paragraphs
	)

	document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
	{body}
	<w:sectPr>
	  <w:pgSz w:w="12240" w:h="15840"/>
	  <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
	</w:sectPr>
  </w:body>
</w:document>'''
	z.writestr('word/document.xml', document_xml)

print(f'Created: {out}')
