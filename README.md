# Brief


## Was ist Brief?
Ein simples Skript, um Arztbriefe aus einem vordefinierten
Aufnahmezettelformat zu generieren. Brief nimmt hierbei Rücksicht
auf die gestellten Diagnosen sowie ggf. Medikamente, um
Absätze zu generieren und Empfehlungen aufzunehmen. Weiterhin
ermöglicht Brief, analog erhobene Daten (Vorbehandlungen, 
BDI-II ähnlichen Fragebogen etc.) einfach zu digitalisieren und
in entsprechende Textpassagen umzuwandeln.

## Download
Unter Windows ist eine ausführbare Datei verfügbar: [Download](./dist/brief_latest.zip).
Vor dem Ausführen muss das Zip-Archiv entpackt werden. Mit Doppelklick auf
brief.exe wird das Programm gestartet. Vor Start sollte in config.txt die Zeile
```
db=.
```
angeglichen werden, sodass sie auf das Verzeichnis der Aufnahmebögen verweist.
Z.B.: 
```
db=C:/Dokumente und Einstellungen/Meine Aufnahmebögen/
```

## Installation
Brief wird als Pythonskript ausgeführt, hierfür wird
eine Installation von Python >=3.12 benötigt. Anschließend kann
main.py in der Konsole mittels
```commandline
>Python main.py
```
ausgeführt werden. Hierfür muss die Konsole sich in dem gleichen
Verzeichnis wie main.py befinden. Unter Windows kann eine Konsole
in dem aktuellen Verzeichnis aus dem Explorer heraus geöffnet
werden (Rechtsklick &#8594; Im Terminal öffnen **oder** Datei &#8594; 
In Windows Powershell öffnen).

Alternativ wird eine ausführbare Datei angeboten, die selbstständig
ein Konsolenfenster öffnet. Die ausführbare Datei muss im gleichen Verzeichnis
wie ihre config.txt Datei liegen.

## Konfiguration
Alle Pfade lassen sich in config.txt anpassen. Standardmäßig
wird das aktuelle Verzeichnis nach folgenden Ordnern durchsucht:
- db: Ordner, in dem sich die Aufnahmebögen als docx-Format befinden. Default
ist das aktuelle Verzeichnis.
- output: Ordner, in dem die generierten Dateien gespeichert werden
- templates: Ordner, in dem sich die Schablonen für die 
Dateigenerierung befinden
  - document_template.xml: XML-Datei im Word Docx-Format, mit welcher
  word/document.xml in der fertig generierten Datei ersetzt wird
  - header1_template.xml: XML-Datei im Word Docx-Format, mit welcher
  word/header1.xml in der fertig generierten Datei ersetzt wird
  - insert_template.xml: XML-Datei, die Textblöcke als Docx-XML beinhaltet,
  die abhängig von Diagnosen oder Medikamenten eingefügt werden können,
  oder Schablonen, mit denen Listen oder Tabellenreihen generiert werden
  können
  - template.docx: Docx-Dateistruktur OHNE word/document.xml und OHNE
  word/header1.xml.

## Schablonen
Brief ist möglichst modular gestaltet, sodass Inhalte einfach verändert
werden können. Hierfür sind die Dateien in ./templates von Interesse:

### Docx-Schablone verändern
Die docx-Datei im ./templates Verzeichnis bietet lediglich die
Grundstruktur der generierten Docx-Datei, sie verändert kaum Inhalte.
Im Idealfall sollte sie aus dem Basisdokument erstellt werden, aus
welchem die entsprechenden word/document.xml und word/header1.xml
Dateien als Grundlagen für die entsprechenden Schablonen (siehe unten)
entnommen wurden. Beide Dateien (word/document.xml und word/header1.xml)
dürfen in der Schablonen-Datei nicht mehr vorhanden sein, sie werden später
durch Brief selbstständig hinzugefügt.

### Dokumentschablone verändern
Standardmäßig sucht Brief nach ./templates/document_template.xml als Grundlage
für die generierte word/document.xml. Es empfiehlt sich, eine gültige 
word/document.xml als Grundlage zu nehmen und diese anzupassen, sofern die
Standarddatei verändert werden soll. Folgende Textfelder werden ersetzt:

- {patient_appellation}: Herr | Frau *Nachname*
- {patient_discharge}: *Entlassdatum, aus Aufnahmebogen gelesen*
- {patient_name}: *Vorname* *Nachname*
- {patient_birthdate}: *Geburtsdatum, aus Aufnahmebogen gelesen*
- {patient_age}: *Errechnetes Alter*
- {patient_height}: *Größe ohne Einheit*
- {patient_weight}: *Gewicht ohne Einheit*
- {patient_bloodpressure}: *Blutdruck ohne Einheit*
- {patient_pulse}: *Herzfrequenz ohne Einheit*
- {patient_address}: *Kommaseparierte Adresse*
- {patient_admission}: *Tag und Monat der Aufnahme, aus Aufnahmebogen gelesen*
- {assigned_doctor}: *Behandelnder Arzt, aus Aufnahmebogen gelesen*
- {assigned_therapist}: *Psychotherapeut, aus Aufnahmebogen gelesen*
- {midas}: *Generierter Text MIDAS-Score*
- {whodas}: *Generierter Text WHODAS-2.0-Score*
- {prev_treatments}: *Generierter Text Vorbehandlungen, inklusive Ärzte, 
Basis- und Akutmedikation sowie nicht-medizinische Behandlungen*
- {self_evaluation}: *Generierter Text Selbstauskunft BDI-II 
und Persönlichkeitsscore*
- {patient_allergies}: *Allergien, aus Aufnahmebogen gelesen*
- {insert_diagnoses}: *XML Liste der gefundenen Diagnosen, aus 
Aufnahmebogen gelesen*
- {base_medication}: *XML Tabellenreihen mit Schmerz-Vormedikation, aus 
Aufnahmebogen gelesen*
- {other_medication}: *XML Tabellenreihen mit sonstiger Vormedikation, 
aus Aufnahmebogen gelesen*

Weiterhin sind grundlegende allgemeine binär gegenderte Ansprachen möglich,
unter anderem:

- {pat_nom}: der Patient | die Patientin
- {pat_nom_cap}: Der Patient | Die Patientin
- {pron_nom}: er | sie

### Header Schablone verändern
Für ./templates/header1_template.xml gilt ähnliches wir für 
document_template.xml, auch hierfür sollte eine docx-generierte
Datei als Grundlage genommen werden. Als Textfeld steht nur

- {patient_data}: *Vorname* *Nachname*, \**Geburtsdatum*

zur Verfügung.

### Insert Schablone verändern
#### Inserts
Der Aufbau der Datei ist relativ egal, relevant sind insert-Tags:
Der Inhalt dieser Tags wird exakt so als XML übernommen, sollte daher
gültiges OfficeOpenXML sein. Attribute des insert-Tags sind:

- for: Beinhaltet ICD10-Kennzeichnung der Diagnose, für welche
der Textbaustein generiert werden soll
- name: Textfeld-Name unter welchem der Textbaustein in
document_template.xml ansprechbar ist (z.B. 
"{migraine_letter_recommendation}")

#### Templates
Template-tags ermöglichen, die Darstellung von Diagnosen und Medikation
zu verändern. Sie beinhalten XML für genau eine Diagnose/ein Medikament.
Das name-Attribut gibt an, ob es für "diagnosis" oder "medication"
angewandt werden soll. Innerhalb der "diagnosis"-template tags stehen
die Textfelder

- {icd10}: ICD10-Kodierung
- {name}: Name der Diagnose (aus Aufnahmebogen gelesen)

zur Verfügung.

Innerhalb der "medication"-template stehen die Textfelder

- {name}: Name des Medikamentes
- {dosage}: Dosierung mit Einheit der Medikation
- {morning}, {noon}, {evening}, {night}: "1" oder "1/2" o.ä. aus dem
Aufnahmebogen gelesene Bezeichnung für den jeweiligen Einnahmezeitpunkt.

zur Verfügung.

