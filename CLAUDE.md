# Garden Park Guest House · Projektbeschreibung für Claude

Diese Datei lesen, bevor am Projekt gearbeitet wird.

## Worum es geht

Neubau der Webseite www.garden-park.co.uk des Garden Park Guest House in Grantown-on-Spey (Cairngorms National Park), geführt von Sarah und Daniel Muccio. Projekt von November 2026 bis Februar 2027, live zum Saisonstart 2027. Umsetzung: Daniel Muccio für AVADAM, Adi (Adrian von Arb) hilft vor allem bei den Fotos. Änderungen nur in Absprache mit Daniel.

Status: **Entwurf.** Für Suchmaschinen gesperrt (`robots.txt` und `noindex`). Erst beim echten Start entfernen.

## Grundlagen (auf Daniels Laptop, E:\Claude\Projekte\Garden Park Guest House Web Page 2027)

- `Garden Park Web Page 2027.md`: Stand, Entscheide, Hosting, Widersprüche.
- `Seitenplan.md`: alle Seiten, Reihenfolge der Startseite, Zimmer-Fakten, Links.
- `Web_page_rewording_the_text.docx`: neueste Textfassung, Grundlage für alle Texte.
- `garden_park_homepage_seo_implementation_brief.docx`: SEO-Brief (H1–H3, interne Links, strukturierte Daten). Achtung: „Open all year“, „Four-poster“ und „selected days“ darin stimmen nicht.
- Brand: E:\Claude\Garden Park Branding (Grün #B0CB1F, Gold-Verlauf, Logo weiss).

## Stil

Der heutige Look von garden-park.co.uk gefällt Daniel und bleibt: dunkle Menüleiste, goldenes Schrift-Logo, grüne Knöpfe, grosse Fotos, Zimmerkarten mit Schatten. Er wird poliert und für 2026–2035 fit gemacht: mehr Luft, grössere ruhige Schrift, kein Text auf unruhigen Fotos, Fakten statt nur Icons. Die Butterfly-Cottage-Seite (butterfly-cottage.co.uk) ist der technische Bauplan.

Pflicht in jedem Projekt: Hell/Dunkel-Modus, Geschwindigkeit immer mit Google PageSpeed Insights (pagespeed.web.dev) prüfen bzw. vor dem Start lokal mit Lighthouse (gleiche Messung, Handy und Computer), keine teuren CSS-Filter wie grosse blur() auf Bildern (lieber vorberechnete Bilder), Back-to-Top mit eigenem, überraschendem Motiv (Daniels Markenzeichen), PageSpeed auf Maximum, Footer „Website by AVADAM“ mit Link auf https://avadam26.github.io/avadam/.

- **Gold ist am Maximum** (Stand 26.11.2026): Deluxe/Superior, die grosse goldene 5 bei den Bewertungen, Frühstücksteller mit Goldrahmen. Faktenleiste (seit 26.11. nach Adis Variante als ruhiges Band mit Trennlinien), Good to know und die Bewertungskacheln sind bewusst ohne Gold; die Bewertungskacheln funkeln nur beim Darüberfahren (Champagner-Glanz). Wünscht Daniel mehr Gold, ihn zuerst daran erinnern, nicht einfach umsetzen.
- Die sechs Kacheln bei The area sind auf allen Geräten hinter „More about the area“ („Less about the area“), Klasse `all-sizes`. Zugeklappt bleibt von „Plan your stay with ease“ nur Titel und erster Satz, „Explore …“ und der Kartenknopf erscheinen erst beim Aufklappen.
- Auf dem Handy sind Packages & news und die Galerie (zeigt nur das Haus bei Nacht) zum Aufklappen (`.m-collapsible` und `.m-toggle`). Am Computer ist alles offen.
- Good to know ist eine kompakte Liste (Name und kurzer Wert), ein Klick zeigt rechts den Text mit grossem grünem Wert und Untertitel; am Anfang ist Opening times offen. Auf dem Handy öffnet sich der Text unter der Zeile.
- Bewegung beim Scrollen: Galeriefotos öffnen sich ruhig von links nach rechts wie ein Vorhang (clip-path, 1,6 s, nach Adis Variante; Erkennung per Scroll, nicht IntersectionObserver), die Teller blenden weich ein, die 5 und die Balken bei den Bewertungen zählen von 0 hoch. Ist der Bereich länger als 3 Sekunden ausser Sicht, startet beides beim nächsten Hinscrollen frisch. Nur mit `translate`/`opacity`, damit nichts springt (CLS 0), und aus bei „reduzierte Bewegung“.
- Handy: oben verschmilzt die Menüleiste mit dem Hero-Foto, nur die Knöpfe bleiben (runder dunkler Hintergrund). Beim Scrollen werden Leiste und kleines Logo in den ersten rund 90 px eingeblendet (`--hb` im Skript), bei offenem Menü ist die Leiste sofort voll da.
- Zimmer kompakt (Idee von Adi): oben eine Reihe mit 6 Zimmern und Butterfly Cottage (Foto, Kategorie, Name). „More room details“ klappt die ausführlichen Zimmerkarten, den Preishinweis und die Butterfly-Karte auf; ein Klick auf ein Zimmer öffnet direkt bei diesem Zimmer. Auf dem Handy zweispaltig und mittig.
- FAQ kompakt: zwei Fragen sichtbar, „More questions and answers“ zeigt alle neun und den Hinweis auf die Karte („Fewer questions and answers“ klappt zu). Alle Fragen bleiben im HTML und in den FAQ-Daten für Google.
- Kartenkachel bei The area ohne Kachel-Schatten, nur feiner Rahmen in der Farbe von „Open the map“. Getting here bei Kontakt ohne Kachel, mit feiner Linie.

## Technik

Reines HTML, CSS und JavaScript, kein PHP, kein WordPress. Packages, Angebote und News pflegen Sarah und Daniel später selber über ein Redaktionsfenster; daraus wird fertiges HTML gebaut (für Google und KIs lesbar, nichts per JavaScript nachladen). Hosting bei twofentons (Katie, Darren), eigenes Control Panel angefragt.

Bestehende Adressen bleiben: `/`, `/de/`, `/grantown-map/`, `/privacy-policy/`, `/cookie-policy/`. Die Karte auf Butterfly (`/grantown/grantown-map.html`) nie ändern, sie steht als QR-Code im Cairngorms-Guide. Garden Park hat eine eigene Kopie der neuesten Karte unter `/grantown-map/` (Quelle: Butterfly-Server-Sicherung vom 12.11.2026 auf E:). Wird die Karte auf Butterfly geändert, die Kopie hier nachziehen. Daniel lädt die Butterfly-Karte selbst per FTP hoch (Datei auf E:), Roger macht dort nichts. Seit 25.11. in beiden Karten: keine Kurzformen im Englischen, Guest/Guests gross, Inverness etwa 50 Minuten. Der Blog bleibt auf Butterfly und wird von der Karte dorthin verlinkt. Links auf die Karte immer relativ (`grantown-map/?v=DATUM`, Versionsnummer bei jeder neuen Kartenversion erhöhen, damit Browser nicht die alte Karte zeigen), damit die Vorschau die neue Karte zeigt. Einzige Ergänzung in der Garden-Park-Kopie: `#distilleries` öffnet direkt die Karte „Speyside Distilleries“, `#gin` springt dort zu den Gin-Kacheln, und Kinrara bekommt zwei einfliegende Kronen für die Preise 2025 und 2026. Sprungziele wie `#golfFishingSection` werden nach dem Laden nochmals angefahren (kleine Funktionen vor `openDestFromHash`, CSS am Ende des Style-Blocks). Beim Nachziehen einer neuen Kartenversion wieder einbauen. Auf der Startseite steht bei The area neben dem Titel eine Kachel mit Kartenvorschau (`img/map-preview-*.webp`, Bildschirmfoto der Karte, der OpenStreetMap-Hinweis muss bleiben). Sprungziele: `#golfFishingSection` (Golf & Fishing), `#travelSection` (Anreise), `#noCarSection` (ohne Auto), `#dest=<id>` (ein Ort).

Sprachen: Englisch (`index.html`) ist die Quelle. Im Menü zeigt die Sprachwahl nur die aktuelle Sprache mit Fahne (SVG, keine Emoji-Fahnen, die zeigt Windows nicht), ein Klick öffnet die Liste; gebaut von `lang_block` im Skript. `/de/`, `/it/`, `/nl/`, `/fr/` werden nie von Hand bearbeitet, sondern mit `python3 tools/build-lang.py` aus `index.html` und den Übersetzungen in `i18n/<sprache>.json` gebaut. Nach jeder Textänderung im Englischen das Skript laufen lassen. Es meldet fehlende und alte Texte, die fehlenden in allen vier Dateien ergänzen. Namen (Zimmer, Wee Fancy Brügel, Generation Getaway, Twixmas, Hogmanay, Butterfly Cottage, Green Tourism, Awards) und „à la minute“ nie übersetzen. Kundenbewertungen bleiben in der Originalsprache. Anrede Deutsch „Sie“, Französisch „vous“, Italienisch „voi“, Holländisch „u“. Deutsch immer „Zweibettzimmer mit zwei Einzelbetten“. Französisch vor ? ein schmales Leerzeichen.

Messen von Anfang an: Google Analytics, Cookie-Banner (Termageddon, Consent Mode v2), Trichter Webseite → Karte → Buchung.

## Beim Start (live) nicht vergessen

- Google Search Console und Google Analytics (mit Consent Mode) erst einbauen, wenn die Seite live ist. Dann Sperre (`noindex`, `robots.txt`) entfernen und Sitemap einreichen.
- Alle Links, die schon im Umlauf sind (Instagram, Facebook, YouTube, Cairngorms-Guide, Mails, Buchungsbestätigung, Butterfly-Seite usw.), mit Zusätzen (`?utm_source=…&utm_medium=…&utm_campaign=…`) versehen, damit Analytics zeigt, woher die Besucher kommen. Vorher mit Daniel eine Liste machen.
- Alle QR-Codes müssen weiter funktionieren: die alten Adressen bleiben (`/`, `/de/`, `/grantown-map/`, `/privacy-policy/`, `/cookie-policy/`, Butterfly `/grantown/grantown-map.html`). Vor dem Umzug mit Daniel alle QR-Codes und ihre Ziele auflisten und nach dem Umzug jeden einmal scannen.
- Erst nach dem Start: Italienisch prüft Daniel, Holländisch und Französisch lassen Muttersprachler gegenlesen, neue Fotos macht Adi in Schottland.

## Fakten (nichts davon ändern ohne Daniel)

- Adresse: Garden Park, 2 Woodside Avenue, Grantown-on-Spey, PH26 3JN. Telefon +44 1479 873235. Mail relax@garden-park.co.uk.
- Geschlossen November bis Februar, ausser zwischen Weihnachten und Neujahr. Nie „Open all year“ schreiben.
- Zimmer: MacDonald (Superior, Super-King-Size, einziges Zimmer mit Badewanne mit Dusche), Grant (Deluxe, King-Size, 1,8 m Dusche mit Regendusche und Handbrause), Fraser und Sutherland (Doppelbett), Mathieson und MacKay (Twin, auf Deutsch immer „Zweibettzimmer mit zwei Einzelbetten“). Erdgeschoss: Sutherland (Walk-in-Dusche mit Regendusche und Handbrause) und Mathieson (Dusche mit 15 cm Absatz). Alle anderen Obergeschoss, mit Dusche. Einzelbelegung in jedem Zimmer möglich.
- Keine festen Preise auf der Seite, Preise nur im Buchungskalender.
- Butterfly Cottage: Selbstverpflegung für 2 Erwachsene plus bis 2 Kinder bis 10 Jahre oder 1 Kind bis 12 Jahre, Doppelbett erhöht mit Platz für Gepäck darunter, Walk-in-Dusche, einzige Unterkunft für Hunde. Eigene Seite butterfly-cottage.co.uk.
- Nicht rollstuhlgängig, mit Gehhilfe machbar.
- Grantown ist die „Capital of Strathspey“, „capital of the Cairngorms“ nur als früherer Beiname.

## Links

Instagram https://www.instagram.com/gardenpark1868 · Facebook https://www.facebook.com/GardenParkGuestHouse/ · YouTube https://www.youtube.com/@scotlandbydan · TripAdvisor https://www.tripadvisor.co.uk/Hotel_Review-g190790-d1749566-Reviews-Garden_Park_Guest_House-Grantown_on_Spey_Aviemore_and_the_Cairngorms_Scottish_Highland.html · Booking.com https://www.booking.com/hotel/gb/garden-park-guest-house.html · Google https://share.google/eFxh1GessZjSeQAQ1

## Regeln

- **Nichts erfinden.** Keine Preise, Angaben oder Bewertungen, die nicht von Daniel oder Sarah kommen. Fehlendes als Platzhalter in eckigen Klammern.
- **Texte:** bestehende Texte übernehmen und nur glätten, nicht neu erfinden, kein Werbe-Englisch. Britisches Englisch. „Guest/Guests“ bewusst gross. Deutsch in Schweizer Schreibweise, immer „ss“, nie „ß“.
- Jede Änderung auf dem Handy und am Computer, hell und dunkel prüfen. Nichts darf seitlich überstehen.
- Vor dem Arbeiten `git pull`, kleine Commits mit deutscher Beschreibung.
- **Commits immer im Namen der Person, die gerade arbeitet**, nie nur als „claude“. Vor dem ersten Commit `git config user.name` und `git config user.email` im Repo setzen. Ist unklar, wer arbeitet, kurz fragen.
  - Dani: `scotlandbydan` mit `317312833+dmuccios24-oss@users.noreply.github.com`, nie mit seiner Gmail-Adresse, sonst blockt GitHub den Push.
  - Adi: `f5yct67kcv-source` mit `284693819+f5yct67kcv-source@users.noreply.github.com`.
- **Arbeit am Ende jeder Sitzung in `main` zurückführen.** Cloud-Sitzungen arbeiten auf einem Zweig `claude/…`: vor Sitzungsende `git pull origin main`, Konflikte lösen, in `main` übernehmen und hochladen. Nur wenn Adi oder Dani ausdrücklich zuerst prüfen wollen, stattdessen einen Pull Request.
- Doku als Absicherung: nach grösseren Schritten die Projekt-Doku in Daniels Obsidian unter „Projekte“ und auf E:\Claude\Projekte\Garden Park Guest House Web Page 2027 nachführen.
