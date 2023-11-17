# Incheck Systeem Hogenschool Rotterdam

Met deze app kunnen leerlingen worden toegevoegd aan klassen 
zodat ze bij een bijeenkomst kunnen inchecken via qr code of http link.
Hierdoor kan de aanwezig heid per leerling bijgehouden worden en kan er 
giezien worden wat de opkomst is per bijeenkomst.

## Inloggen
Voor het inloggen zijn twee verschillende accounts gemaakt, een student en een docent.
De docent heeft accounts met admin rechten en zonder. Leerling accounts hebben geen admin rechten.
Bij aanmaakt nieuwe gebruiker word er een standaard wachtwoord aangemaakt deze is:
werkplaats3

### Student
Student inlog gegevens worden gegenereerd vanuit hun studentcode voor willekeurig aangemaakte studenten lopen van 1 tot 1000.

### Docent
Docent accounts worden aangemaakt met het email dat de opleiding aan de docent heeft gegeven.
Admin docent is t.maijer@hr.nl
Andere docenten hebben geen admin rechten

### Wachtwoord veranderen
Er is functionaliteit om je wachtwoord te veranderen.
Bij invoer login naam word er een mail gestuurd naar het email account dat hoort bij het account.
Mail bevat token om wachtwoord te veranderen.

## Incheck funtionaliteit
De incheck word geregeld met een qr. De code die verzonden word verwijst naar de studenten pagina,
en geeft de meeting id mee. Als bij inlog deze word opgehaald word de leerling ingecheckt voor de juiste bijeenkomst.

## Bijeenkomst aanmaak functionaliteit
De lijst met opleidingen word opgehaald uit de database en word door middel van een jinja loop gepresenteerd op het scherm.
De studenten lijst word door middel van JS Fetch live gevormd bij het intypen van een naam.
Het form verwijst naar een JS Fetch die het POST request regelt.
Studenten worden met Fetch op het schedule item gepresenteerd.

## Docenten menu
Agenda word met JS Fetch opgehaald en gepresenteerd op het scherm.
Admin heeft hier extra functionaliteit om naar account creatie scherm te komen.
Docent heeft mogelijkheid om een les te verwijderen door bijvoorbeeld een fout.
Ook kan de docent de bijeenkomst cancelen bij bijvoorbeeld uitval of afwezigheid docent. 

## Student pagina
Student kan ook inloggen als hij geen incheck moment heeft. Dan word alleen agenda getoond.
Bij incheck krijgt student te zien voor welke les er is ingecheckt. Na verstuden antwoord 
verdwijnt les informatiue en is allen het rooster nog zichtbaar.
Leerling kan zich in de agenda afmelden voor aankomende lessen.
Agenda word met een JS Fetch loop gepresenteerd op het scherm.

## Beamer scherm
Op het beamer scherm word een qr code gepresenteerd voor de incheck.
Een lijst met wisselknopjes laat zien welke studenten er aanwezig, afwezig en afgemeld zijn.
Ook is er een knopje om de gegeven reacties te bekijken van de leerlingen. Deze zijn in dit geval
anoniem.
De link van de qrcode is opgesteld uit de basis url en het id van de meeting.
