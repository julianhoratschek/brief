from patient import Patient
from docx import (DocxParagraph, DocxRunProperties,
                  DocxIdentationProperty, DocxJustificationProperty,
                  DocxFontProperty, DocxSizeProperty,
                  DocxNumberingProperty, DocxTabsProperty,
                  DocxBigProperty, melt)


def get_inserts(patient: Patient):
    font = DocxFontProperty()
    jc = DocxJustificationProperty()
    size18 = DocxSizeProperty(18)

    rpr18 = DocxRunProperties([font, size18])

    ppr_diagnoses = [DocxIdentationProperty(1134, 1134),
                     jc,
                     rpr18]

    diagnoses_paragraphs: list[DocxParagraph] = []

    migraine_with_aura_letter_recommendations = []
    cluster_base_recommendations = []
    cluster_letter_recommendations = []
    cluster_new_episode = []
    tth_letter_recommendations = []

    for name, icd10 in patient.diagnosis:
        diagnoses_paragraphs.append(DocxParagraph(ppr_diagnoses).run(f"{icd10}\t{name}"))

        match icd10:
            # Migraine with aura
            case 'G43.1':
                migraine_with_aura_letter_recommendations = [
                    DocxParagraph([rpr18]).run("Bei ")
                                          .run("Migräne mit Aura", rpr18.having(DocxBigProperty()))
                                          .run(" ist der Einsatz von Triptanen während einer Aura kontraindiziert. "
                                               "Hier empfiehlt sich die Einnahme von Akutanalgetika wie "
                                               "Novaminsulfon® (Metamizol) 40° bis zu 4x täglich. Alternativ ist "
                                               "Diclofenac 20°, maximal 3x täglich möglich. Nach sicher abgeklungener "
                                               "Aurasymptomatik kann der Einsatz von Triptanen erfolgen.")
                ]

            # Cluster
            case 'G44.0':
                ppr_num = [DocxNumberingProperty(0, 21),
                           DocxTabsProperty([743, 6804]),
                           DocxRunProperties([font, DocxSizeProperty(16)])]

                ppr_ltr = [jc, rpr18]

                ppr_big = [DocxRunProperties([font, size18, DocxBigProperty()])]
                ppr18 = [DocxRunProperties([font, size18])]

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
                                               "schrittweise Aufdosierung"),
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
                                               "Belastungs-EKG zeitnah durchführen lassen"),
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
                    DocxParagraph(ppr_ltr).run("Die Dosierung des Verapamil retard (Isoptin®) sollte dem "
                                               "Krankheitsverlauf angepasst werden. Bei unzureichender Wirkung kann "
                                               "ggf. eine weitere Dosissteigerung unter Beachtung vom "
                                               "Verträglichkeits- und Nebenwirkungsspektrum erfolgen, die Tagesdosis "
                                               "von 960 mg pro Tag nicht überschreitend. Unter Verapamil-Medikation "
                                               "bitten wir um regelmäßige kardiologische Kontrollen mittels EKG und "
                                               "Echokardiographie sowie bei jeder Dosissteigerung. Dosisreduktion des "
                                               "Verapamils nach 6-8 attackenfreien Wochen, hierbei schrittweise "
                                               "Ausdosieren."),
                    DocxParagraph(ppr_ltr),
                    DocxParagraph(ppr_ltr).run("Die Attackenbehandlung des Clusterkopfschmerzes kann durch Inhalation "
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
                rpr = DocxRunProperties([font, size18])
                ppr18 = [jc, rpr]
                big_prop = DocxBigProperty()

                tth_letter_recommendations = [
                    DocxParagraph(ppr18).run("Bei der Behandlung chronischer ")
                                        .run("Kopfschmerzen vom Spannungstyp", rpr.having(big_prop))
                                        .run(" sind Verhaltensmaßnahmen in Form von Stressreduktion, "
                                             "Entspannungsverfahren, Sporttherapie, Biofeedback, Wärmeanwendungen, "
                                             "Massageanwendungen sowie ggf. eine Behandlung einer oromandibulären "
                                             "Dysfunktion ein zentraler Baustein."),
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18).run("Die hier vermittelten nicht-medikamentöse Therapieoptionen bei ")
                                        .run("Kopfschmerzen vom Spannungstyp", rpr.having(big_prop))
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
                    DocxParagraph(ppr18),
                    DocxParagraph(ppr18).run("Kopfschmerzen vom Spannungstyp", rpr.having(big_prop))
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

    return {
        "insert_diagnoses": melt(diagnoses_paragraphs),
        "migraine_with_aura_letter_recommendations": melt(migraine_with_aura_letter_recommendations),
        "cluster_base_recommendations": melt(cluster_base_recommendations),
        "cluster_new_episode": melt(cluster_new_episode),
        "cluster_letter_recommendations": melt(cluster_letter_recommendations),
        "tth_letter_recommendations": melt(tth_letter_recommendations),
    }

