from patient import Patient
from docx import (DocxParagraph, DocxRunProperties,
                  DocxIdentationProperty, DocxJustificationProperty,
                  DocxFontProperty, DocxSizeProperty,
                  DocxNumberingProperty, DocxTabsProperty, DocxHighlightProperty, DocxRun,
                  DocxBigProperty, melt)


def get_inserts(patient: Patient):
    # Paragraph Properties
    jc = DocxJustificationProperty()
    num = DocxNumberingProperty(0, 21)

    # Run Properties
    font = DocxFontProperty()
    size18 = DocxSizeProperty(18)
    size16 = DocxSizeProperty(16)
    yellow = DocxHighlightProperty("yellow")
    big = DocxBigProperty()

    rpr18 = DocxRunProperties([font, size18])
    rpr16 = DocxRunProperties([font, size16])

    ppr_diagnoses = [DocxIdentationProperty(1134, 1134),
                     jc,
                     rpr18]
    ppr18 = [rpr18]
    ppr18_jc = [jc, rpr18]

    diagnoses_paragraphs: list[DocxParagraph] = []

    migraine_with_aura_letter_recommendations = []
    cluster_base_recommendations = []
    cluster_letter_recommendations = []
    cluster_new_episode = []
    tth_letter_recommendations = []
    overuse_base_recommendations = []
    overuse_letter_paragraph = DocxParagraph([DocxTabsProperty([1701, 2268, 6804]), jc, rpr18])
    overuse_letter_definition = []
    overuse_additional_risk = []
    overuse_letter_recommendations = []
    overuse_closing_statement = []

    for name, icd10 in patient.diagnosis:
        diagnoses_paragraphs.append(DocxParagraph(ppr_diagnoses).run(f"{icd10}\t{name}"))

        match icd10:
            # Misuse of Medication
            case 'F55.2':
                hi = rpr18.having(yellow)
                if not overuse_letter_definition:
                    overuse_letter_definition.append(overuse_letter_paragraph)

                (overuse_letter_paragraph
                 .run("Es besteht ein Fehlgebrauch durch nicht-selektive Anwendung der Triptane bei Kopfschmerz "
                      "vom Spannungstyp und Medikamentenübergebrauchskopfschmerzen. ", hi)
                 .run("Es besteht ein Fehlgebrauch aufgrund nicht spezifischer Differenzierung der "
                      "Akutmedikation in der Akutbehandlung der Migräne, Spannungskopfschmerzen und der "
                      "Intervallkopfschmerzen. ", hi)
                 .run("Es besteht ein Fehlgebrauch, indem Triptane erst dann eingenommen werden, wenn die "
                      "Migräneattacke ihre höchste Kopfschmerzintensität erreicht hat. ", hi)
                 .run("Es besteht ein Fehlgebrauch aufgrund Wiederholung des primär eingesetzten Triptans "
                      "bei primärer Unwirksamkeit im Anfall. ", hi)
                 .run("Es besteht ein Fehlgebrauch bei der Anwendung von Escape-Medikation bei primärer "
                      "Unwirksamkeit des Triptans. ", hi)
                 .run("Bei status migraenosus werden über 5 Tage täglich Schmerzmitteln und Triptane eingesetzt.", hi))

            # Migraine with aura
            case 'G43.1':
                migraine_with_aura_letter_recommendations = [
                    DocxParagraph(ppr18).run("Bei ")
                                        .run("Migräne mit Aura", rpr18.having(big))
                                        .run(" ist der Einsatz von Triptanen während einer Aura kontraindiziert. "
                                             "Hier empfiehlt sich die Einnahme von Akutanalgetika wie "
                                             "Novaminsulfon® (Metamizol) 40° bis zu 4x täglich. Alternativ ist "
                                             "Diclofenac 20°, maximal 3x täglich möglich. Nach sicher abgeklungener "
                                             "Aurasymptomatik kann der Einsatz von Triptanen erfolgen.")
                ]

            # Cluster
            case 'G44.0':
                ppr_num = [num,
                           DocxTabsProperty([743, 6804]),
                           rpr16]

                ppr_big = [rpr18.having(big)]

                cluster_base_recommendations = [
                    DocxParagraph(ppr_num).run("Kontinuierlich Kopfschmerzkalender führen"),
                    DocxParagraph(ppr_num).run("Die Dosierung des Verapamils sollte dem Krankheitsverlauf angepasst "
                                               "werden. Bei unzureichender Wirkung kann ggf. eine weitere "
                                               "Dosissteigerung unter Beachtung von Verträglichkeit und "
                                               "Nebenwirkungsspektrum erfolgen, die Tagesdosis von 960 mg pro Tag "
                                               "nicht überschreitend"),
                    DocxParagraph(ppr_num).run("Unter der aktuellen Verapamil-Medikation bitten wir um regelmäßige "
                                               "kardiologische Kontrollen mittels EKG und Echokardiographie sowie bei "
                                               "jeder Dosissteigerung"),
                    DocxParagraph(ppr_num).run("Wegen des chronischen Verlaufs der Clusterkopfschmerzen ist die "
                                               "Einnahme von Verapamil zeitlich nicht befristet. Dosisreduktion des "
                                               "Verapamils nach 4-6 attackenfreien Wochen, hierbei schrittweise "
                                               "ausdosieren. Bei erneutem Ausbrechen von Clusterattacken erneute "
                                               "schrittweise Aufdosierung"),
                    DocxParagraph(ppr_num).run("Wir bitten um kardiologische Kontrolluntersuchung der o.g. Medikation "
                                               "mit Echokardiographie, Langzeitbelastungs-EKG zeitnah durchzuführen"),
                    DocxParagraph(ppr_num).run("Da Clusterkopfschmerz eine Schmerzform ist die überdurchschnittlich "
                                               "häufig bei Rauchern auftritt und durch Alkohol triggerbar ist, "
                                               "empfahlen wir dringend eine Nikotin- und Alkoholabstinenz"),
                    DocxParagraph(ppr_num).run("Kein Nitrospray bei Clusterkopfschmerzen "),
                    DocxParagraph(ppr_num).run("Wir bitten um Kontrolluntersuchung der o.g. Medikation"),
                    DocxParagraph(ppr_num).run("Dosiserhöhung des Lithiums an die Attackenhäufigkeit angepasst. "
                                               "Maximaler Blutspiegel 0,6 mmol/l. Eine Dosisreduktion des Lithiums "
                                               "frühestens nach 4-6 attackenfreien Wochen. Hierbei schrittweise "
                                               "ausdosieren. Dosisreduktion von Verapamil nach Absetzen des Lithiums "
                                               "von weiteren 4-6 attackenfreien Wochen, hierbei nur schrittweise "
                                               "ausdosieren. Bei erneutem Ausbruch von Clusterattacken erneute "
                                               "schrittweise Aufdosierung", rpr16.having(yellow)),
                    DocxParagraph(ppr_num).run("Die Bestimmung des Serumlithiumspiegels sollte in den ersten 4 Wochen "
                                               "wöchentlich vorgenom-men werden, danach ggf. bei weiterer Einnahme im "
                                               "ersten halben Jahr 1x monatlich und später im vierteljährlichen "
                                               "Abstand. Die Bestimmung des Serumlithiumspiegels sollte möglichst "
                                               "genau 12 Stunden nach der letzten Einnahme erfolgen. "
                                               "Zwecksmäßigerweise wird die Bestimmung am Mor-gen vor der weiteren "
                                               "Tablettengabe durchgeführt. Wir bitten um eine sorgfältige Überwachung "
                                               "des Patienten während der Lithiummedikation. Folgende Untersuchungen "
                                               "werden gemäß Fachinformation jährlich empfohlen: T3, T4, TSH basal, "
                                               "ggf. TAH-Test, Natrium, Kalium und Calciumbestim-mung, 24 "
                                               "Stundenurinvolumen, Kreatinin-Clearens, EKG, EEG, Urinanalyse, "
                                               "Blutdruckmessung, Blutbild und ggf. Überprüfung der rhenalen "
                                               "Konzentrationsleistung, Desmopressin-Test und eine vierteljährliche "
                                               "Messung von Körpergewicht und Halsumfang. Bitte kardiologische "
                                               "Kontrolluntersuchung mit Echokardiographie, Langzeit- und "
                                               "Belastungs-EKG zeitnah durchführen lassen", rpr16.having(yellow)),
                ]

                cluster_new_episode = [
                    DocxParagraph(ppr_big).run("Vorgehen bei neuer aktiver Clusterperiode"),
                    DocxParagraph(ppr_big),
                    DocxParagraph(ppr_big).run("I. Verhaltensregeln"),
                    DocxParagraph(ppr_big),
                    DocxParagraph(ppr18).run("Kein Alkohol, erst wieder, wenn 4 Wochen attackenfrei"),
                    DocxParagraph(ppr18).run("- Kein Nikotin"),
                    DocxParagraph(ppr18).run("- Keine Nitrate"),
                    DocxParagraph(ppr18).run("- Kein Nitrospray, keine Nitrotabletten"),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr_big).run("II. Medikamentöse Vorbeugung (aktuell, Anpassung in ca. 6 Wochen "
                                               "nach Rücksprache):"),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18).run("Isoptin RR (Wirkung tritt nach ca. 7 Tagen ein)"),
                    DocxParagraph(ppr18).run("- 8 Uhr: 240 mg"),
                    DocxParagraph(ppr18).run("- 20 Uhr: 240 mg"),
                    DocxParagraph(ppr18).run("Wenn attackenfrei, kann nach 6 Wochen jeweils eine halbe Tablette "
                                             "Isoptin pro Woche abdosiert werden."),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18).run("Zusätzlich Prednisolongabe initial:"),
                    DocxParagraph(ppr18).run("- Prednisolon (Decortin H) Tabletten à 20 mg (N2=50 Stück)"),
                    DocxParagraph(ppr18).run("- Dazu Pantoprazol 40 mg am Morgen, Magenschutz (N2=50 Stück)"),
                    DocxParagraph(ppr18).run("- Zur Nacht für 4 Tage Dalmadorm"),
                    DocxParagraph(ppr18).run("- Decortin jeweils am Morgen nach dem Frühstück in folgender "
                                             "absteigender Dosierung:"),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18).run("1.-2. Tag\t100 mg\t\t5 Tabletten zu 20 mg"),
                    DocxParagraph(ppr18).run("3.-4. Tag\t80 mg\t\t4 Tabletten zu 20 mg"),
                    DocxParagraph(ppr18).run("4.-6. Tag\t60 mg\t\t3 Tabletten zu 20 mg"),
                    DocxParagraph(ppr18).run("7.-8. Tag\t40 mg\t\t2 Tabletten zu 20 mg"),
                    DocxParagraph(ppr18).run("9.-10. Tag\t20 mg\t\t1 Tablette zu 20 mg"),
                    DocxParagraph(ppr18).run("11.-12. Tag\t10 mg\t\t1/2 Tablette zu 20 mg"),
                    DocxParagraph(ppr18).run("dann absetzen"),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr_big).run("III. Behandlung der akuten Cluster-Attacke"),
                    DocxParagraph(ppr_big),
                    DocxParagraph(ppr18).run("- Sumatriptan 3 oder 6 mg s.c. mit Autoinjektor (Alternativ auch 2 "
                                             "oder 4 mg mit Fertigspritze)"),
                    DocxParagraph(ppr18).run("- Sauerstoff 10 Liter/min über 10 Minuten"),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18),
                ]

                cluster_letter_recommendations = [
                    DocxParagraph(ppr18_jc).run("Die Dosierung des Verapamil retard (Isoptin®) sollte dem "
                                               "Krankheitsverlauf angepasst werden. Bei unzureichender Wirkung kann "
                                               "ggf. eine weitere Dosissteigerung unter Beachtung vom "
                                               "Verträglichkeits- und Nebenwirkungsspektrum erfolgen, die Tagesdosis "
                                               "von 960 mg pro Tag nicht überschreitend. Unter Verapamil-Medikation "
                                               "bitten wir um regelmäßige kardiologische Kontrollen mittels EKG und "
                                               "Echokardiographie sowie bei jeder Dosissteigerung. Dosisreduktion des "
                                               "Verapamils nach 6-8 attackenfreien Wochen, hierbei schrittweise "
                                               "Ausdosieren."),
                    DocxParagraph(ppr18_jc),
                    DocxParagraph(ppr18_jc).run("Die Attackenbehandlung des Clusterkopfschmerzes kann durch Inhalation "
                                               "von Sauerstoff 15 l/min über 15 Minuten unter Verwendung einer "
                                               "Gesichtsmaske sowie bei Wirkungslosigkeit durch die Verwendung eines "
                                               "Triptans mit schnellem Wirkungseintritt, z.B. Migra-Pen® (Sumatriptan "
                                               "3 mg) als Autoinjektor s.c. oder 4 mg Fertigspritze erfolgen. Hier "
                                               "ist darauf zu achten, dass die Maximaldosis von Sumatriptan in 24 "
                                               "Stunden 12 mg s.c. beträgt. Im Gegensatz zur Migränebehandlung mit "
                                               "Triptanen besteht jedoch keine Höchstgrenze der Anwendung in Tagen "
                                               "pro Monat, da medikamenteninduzierte Kopfschmerzen bei "
                                               "Triptanübergebrauch auf dem Boden von Clusterkopfschmerzen bisher "
                                               "nicht beschrieben sind.")
                ]

            # Tension Type Headache
            case 'G44.2':
                tth_letter_recommendations = [
                    DocxParagraph(ppr18_jc).run("Bei der Behandlung chronischer ")
                                           .run("Kopfschmerzen vom Spannungstyp", rpr18.having(big))
                                           .run(" sind Verhaltensmaßnahmen in Form von Stressreduktion, "
                                                "Entspannungsverfahren, Sporttherapie, Biofeedback, Wärmeanwendungen, "
                                                "Massageanwendungen sowie ggf. eine Behandlung einer oromandibulären "
                                                "Dysfunktion ein zentraler Baustein."),
                    DocxParagraph(ppr18_jc),
                    DocxParagraph(ppr18_jc).run("Die hier vermittelten nicht-medikamentöse Therapieoptionen bei ")
                                           .run("Kopfschmerzen vom Spannungstyp", rpr18.having(big))
                                           .run(" sollten auch ambulant fortgesetzt werden. "
                                                "Diese beinhalten eine Reduktion psychischer Stressoren, eine Reduktion "
                                                "muskulärer Stressoren, die Behandlung von Angst und Depression sowie die "
                                                "Therapie einer oromandibulären Dysfunktion. Die diesbezüglichen "
                                                "Strategien schließen Entspannungsverfahren wie die Progressive "
                                                "Muskelrelaxation, im Biofeedback erlernte Strategien, "
                                                "Stressbewältigungskompetenzen, Lerneinheiten aus Patientenseminaren "
                                                "sowie sporttherapeutische Aktivitäten ein. Physikalische "
                                                "Therapiemaßnahmen umfassen die Thermotherapie, Physiotherapie, "
                                                "TENS-Behandlung sowie Reiztherapie. Üblicherweise ist der chronische "
                                                "Kopfschmerz vom Spannungstyp nur nach mehrmonatiger intensiver und "
                                                "nachhaltiger Behandlung zu verbessern."),
                    DocxParagraph(ppr18_jc),
                    DocxParagraph(ppr18_jc).run("Kopfschmerzen vom Spannungstyp", rpr18.having(big))
                                           .run(" sollten möglichst nur in Ausnahmefällen, "
                                                "maximal jedoch an 10 Tagen im Monat analgetisch behandelt werden, um die "
                                                "Entstehung eines medikamenteninduzierten Dauerkopfschmerzes zu "
                                                "vermeiden. Die medikamentöse Akuttherapie muss darauf ausgerichtet sein, "
                                                "einen Kopfschmerz bei Medikamentenübergebrauch als Komplikation zu "
                                                "vermeiden. Daher ist vorzugsweise die Anwendung von Pfefferminzöl in "
                                                "alkoholischer Lösung (z. B. Euminz N) zu empfehlen, "
                                                "Non-Opioid-Analgetika und Opioid-Analgetika im eigentlichen Sinn "
                                                "sollten vermieden werden. Zur Therapiekontrolle sollte der "
                                                "Kopfschmerzkalender oder die Migräne-App kontinuierlich geführt werden, "
                                                "um sowohl Kopfschmerzsymptome, Medikamenteneinnahme als auch "
                                                "Therapieeffekte im Verlauf zu protokollieren."),
                ]

            # Medication Overuse
            case 'G44.4':
                ppr_num = [DocxNumberingProperty(0, 21),
                           DocxIdentationProperty(601, 241),
                           rpr18]
                rpr18_hi = rpr18.having(yellow)
                ppr_hi = [jc, rpr18_hi]

                overuse_base_recommendations = [
                    DocxParagraph(ppr_num).run("Wir empfehlen die ambulante Fortführung der ")
                                          .run("Analgetikapause für insgesamt vier Wochen", rpr18.having(DocxBigProperty()))
                                          .run(". Medikamentenpause heißt: Alle Medikamente für die Akutbehandlung von "
                                               "Kopfschmerzen dürfen für einen bestimmten Zeitraum nicht eingenommen "
                                               "werden. Die Pause hat nach spätestens vier bis sechs Wochen ihr Ziel "
                                               "erreicht und kann beendet werden. Attacken können dann wieder mit "
                                               "Akutmedikation behandelt werden. Eine medikamentöse Attackentherapie "
                                               "kann auch dann wieder beginnen. Nach Abschluss der Analgetikapause "
                                               "sollte eine Reevaluation der Kopfschmerzen und entsprechende "
                                               "Diagnosesicherung erfolgen.")
                ]

                if not overuse_letter_definition:
                    overuse_letter_definition.append(overuse_letter_paragraph)

                # Prepend Overuse sentence in paragraph
                overuse_letter_paragraph.runs.insert(0, DocxRun(
                    "Der Einsatz von Schmerzmitteln und/oder Triptanen an mehr als 10 Tagen "
                    "im Monat überschreitet die Grenzschwellen für die Entstehung von "
                    "Kopfschmerzen bei Medikamentenübergebrauch. ", rpr18))

                overuse_additional_risk = [
                    DocxRun("Eine analgetische Behandlung dieser ebenfalls mit Schmerzen einhergehenden "
                            "Erkrankungen interferiert gravierend mit der Behandlung der chronischen Migräne. "
                            "Es besteht eine Aufrechterhaltung und weitere Verstärkung des sowieso bestehenden "
                            "Kopfschmerzes bei Medikamentenübergebrauch.", rpr18)
                ]

                overuse_letter_recommendations = [
                    DocxParagraph(ppr_hi).run("Mit Cortison:", rpr18_hi.having(big)),
                    DocxParagraph(ppr_hi).run("Wir führten eine konsequente ")
                                         .run("Medikamenten-Einnahmepause", rpr18_hi.having(big))
                                         .run(" für jegliche Kopfschmerzakutmedikation durch. Zur Erleichterung der zu "
                                              "erwartenden Umstellungsreaktion erfolgte eine befristete intravenöse "
                                              "und orale Gabe von Prednisolon. Zum Einsatz kamen ebenfalls "
                                              "Dimenhydrinat und Melperon, sowie Infusionen mit Dimenhydrinat "
                                              "und Magnesium."),
                    DocxParagraph(ppr_hi),
                    DocxParagraph(ppr_hi).run("Ohne Cortison:", rpr18_hi.having(big)),
                    DocxParagraph(ppr_hi).run("Wir führten eine konsequente ")
                                         .run("Medikamenten-Einnahmepause", rpr18_hi.having(big))
                                         .run(" für jegliche Kopfschmerzakutmedikation durch. Dabei wurde auf eine "
                                              "intravenöse und orale Gabe von Prednisolon nach einem festen "
                                              "Zeitschema verzichtet. Bedarfsweise erhielt die Patientin Medikamente "
                                              "zur Schmerzdistanzierung.")
                ]

                overuse_closing_statement = [
                    DocxParagraph(ppr_hi).run("Des Weiteren empfehlen wir die ambulante Fortführung der ")
                                         .run("Analgetikapause für insgesamt vier Wochen", rpr18_hi.having(big))
                                         .run(patient.gender.apply(". In dieser Phase kann es sinnvoll sein {pat_nom} "
                                                                   "arbeitsunfähig zu schreiben."))
                ]

    return {
        "insert_diagnoses": melt(diagnoses_paragraphs),
        "migraine_with_aura_letter_recommendations": melt(migraine_with_aura_letter_recommendations),
        "cluster_base_recommendations": melt(cluster_base_recommendations),
        "cluster_new_episode": melt(cluster_new_episode),
        "cluster_letter_recommendations": melt(cluster_letter_recommendations),
        "tth_letter_recommendations": melt(tth_letter_recommendations),
        "overuse_base_recommendations": melt(overuse_base_recommendations),
        "overuse_letter_definition": melt(overuse_letter_definition),
        "overuse_additional_risk": melt(overuse_additional_risk),
        "overuse_letter_recommendations": melt(overuse_letter_recommendations),
        "overuse_closing_statement": melt(overuse_closing_statement)
    }

