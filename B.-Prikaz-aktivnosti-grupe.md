# Dnevnik sastajanja

### Prvi timski sastanak
Datum: 12. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic

Teme sastanka:
- formiranje tima, upoznavanje, dogovor oko voditelja tima (izabrana Mia Malović)

- dogovor oko podjela uloga unutar tima (M.Malović, I.Džepina - dokumentacija; D.Gavranić- full stack; V.Milanović, R.Gulan - front-end; D.Žic, V.Ružić - back-end)

- dogovor oko metoda komunikacije (uspostava Discord servera, dogovor oko uspostave Notion workspace-a)

- dogovor oko vremena događanja redovnih tjednih sastanaka (petkom popodne)

- rasprava oko korištenja određenih arhitektura ovisno o znanjima članova

### Prvi sastanak dokumentacijskog tima
Datum: 12. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić

Teme sastanka:

- prolaženje aktivnosti kroz dane na temelju preporuka profesora i prezentacija predmeta
    - dogovorili se oko podjele rada izrade prve verzije funkcijskih i nefunkcijskih zahtjeva
    - dogovorili se da nakon prvotne verzije krećemo u diskusiju o istima na razini tima; nakon toga krenuti izrađivati prve Use Case dijagrame do kraja tjedna 13-19.10.
    - organizacija i uspostava Notiona

### Drugi timski sastanak

Datum: 15. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, V.Milanović, V.Ružić, D.Žic

Teme sastanka: 
- prošli prvu verziju funkcijskih specifikacija i raspravili ih
    - dodatno definirali određene specifikacije vezane uz registraciju, dostavu i udruge
    - dogovorili se oko prilagođenja prioriteta funkcionalnostima vezanima uz udruge
- raspravili izvedbu ostalih platformi sa sličnim specifikacijama i namjenama te diskutirali o sličnostima i razlikama tih platformi u usporedbi s našim projektom
- diskutirali pitanja koja imamo za demonstratora / asistenticu vezana uz implementaciju platforme i nužnost uspostave određenih funkcionalnosti

### Treći timski sastanak

Datum: 17. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic

Teme sastanka:
- dodali i uklonili određene funkcijske specifikacije u skladu sa razgovorom sa asistenticom na labosu (uklonili specifikacije vezane uz cijenu članstva, dodatno objasnili funkcijske specifikacije vezane uz udruge, pojednostavili specifikacije vezane uz plaćanje poštarine itd.)
- raspravili i izradili user journey dijagrame za svakog dionika (korisnik primatelj, korisnik darivatelj roditelj i korisnik darivatelj udruga i admin) 
- dogovoreno da D.Gavranić u suradnji s front-end timom (R.Gulan + V.Milanović) krenu u izradu Wireframe-ova kako bi se dodatno razjasnile nejasnoće vezane uz User Journey; Docs tim (M.Malović + I.Džepina) kreće u izradu UC opisa i dijagrama
- dogovoreno da će nakon jasnijih smjernica, biti smišljena arhitekturu koja će pokriti sve dogovoreno (Back-end tim zadatak)
- dogovoreno da će nakon što se riješi pitanje arhitektura biti potreban sastanak gdje će biti osmišljen Kanban, dodijeljeni zadatci i približno određen rok izrade

### Prvi sastanak backend tima

Datum: 22. listopada 2025.

Prisustvovali: D.Gavranić, V.Ružić, D.Žic

Teme sastanka: 
- postavljeni alati za programiranje (PyCharm, Python, Django template itd.)
- dogovorili sljedeće korake:
    - priprema ER dijagrama i osnovnih modela
    - pregled literature i proučavanje Django mogućnosti
- ukratko diskutirali arhitekturu Djanga i zašto smo ga odabrali

### Sastanak o definiranju modela

Datum: 24. listopada 2025.

Prisustvovali: V.Ružić, D.Žic

Teme sastanka: 
- odredili i raspravili moguće modele za projektnu stranicu
- pregledali kolizije te veze između baza podataka
- provjerili koheziju između modela i smislenost istih

### Četvrti timski sastanak: finalizacija (N)FZ 

Datum: 25. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic

Teme sastanka:

- napravljen pregled FZ/NFZ i predložene promjene za FZ i NFZ oko kojih smo se složili
    - skraćeni opisi većine FZ, preciznije definirane NFZ (npr. specificirani protokoli koji koristimo, preciznije specificirano u kojem roku sustav treba reagirati na podražaj i koliko treba biti online i sl.)
- dogovorena arhitektura sustava i daljnji planovi rada za implementaciju
    - dogovorena suradnja oko izrade dokumenta o objašnjenju donesenih odluka o arhitekturi sustava

### Peti timski sastanak: kratka koordinacija
Datum: 29. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- zbog poteškoća kod pushanja promjena na Githubu, dogovoreno da će Domagoj i Mia biti uključeni u deploy proces
- backend tim čeka frontend da započne s izradom dizajna, u međuvremenu isproban Django Administration kako bi se olakšala implementacija administratorskih ovlasti - Users (UserList, deleteUser i sl.)
- dogovoreno da će dokumentacijski tim napraviti izmjene na obrascima uporabe vezane uz prijavu i registraciju

### Šesti timski sastanak
Datum: 31. listopada 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic

Teme sastanka: 

- komunicirali novosti vezane uz projekt u skladu s konzultacijama na sastanku na laboratorijskoj vježbi
    - dogovorili uklanjanje administratorskog nadziranja chata
    - dogovorili izmjene u UC dijagramima u skladu s literaturom (izmjene dijagrama prijave i odjave, izmjene dijagrama primopredaje jer određene relacije proširenja nisu točne i sl.)
    - započeli izradu sekvencijskih dijagrama
- složili se oko dizajna login stranice i drugih web-stranica unutar platforme, frontend tim nastavio izradu dogovorenog dizajna
- dogovorili se oko toga da ćemo minimalno uz funkcionalnost logina implementirati sustav objave oglasa do prve predaje, backend tim nastavio istraživanje vezano uz implementaciju sustava OAuth 2.0
    - idealno do kraja 6. tjedna tj. do labosa u 6. tjednu implementirali bi navedeno kako bi imali vremena za konzultacije, popravke i potrebno testiranje funkcionalnosti
- otvorili Kanban na Github Projectsu i uspostavili timeline projekta do kraja 7. tjedna

### Sedmi timski sastanak
Datum: 7. studenoga 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- dogovoreno da će najkasnije do utorka u ponoć biti gotova implementacija potrebnih funkcionalnosti, u srijedu testiranje i četvrtak zadnji popravci
    - za ručne testove potrebno napisati scenarije, očekivano ponašanje itd.
        - dogovoreno da front-end i back-end tim u suradnji izrađuju navedeno
- dogovoreno da ER dijagrami moraju biti gotovi do ponedjeljka
- dogovoreno spajanje FE i BE - Domagoj odrađuje što je još potrebno od spajanja, sinkronizacija s BE/FE početkom sljedećeg tjedna
- dogovoreno da ćemo prije predaje pregledati prezentacije, osigurati da imamo sve potrebno
    - dogovoreno da ćemo na još jednu provjeru u ponedjeljak slati UC, sekvencijske dijagrame
- dogovoreno da ćemo što prije izraditi model baze podataka, iz toga generirati ERD dijagram i tablice → delegirano back-endu
- dogovoreno da backend tim izrađuje klasne dijagrame najkasnije do utorka
- donijeli određene odluke vezano uz ER dijagram - razriješili timske konflikte vezane uz nasljeđivanje i elemente dijagrama
    - dodan atribut "wishlist" u campaign, dogovoreno da će se "picture" (slike) pohranjivati kao json field, a ne kao novi atribut
    - cijena dostave dio istog objekta: zahtjeva za donacijom
    - tablica za zahtjeve u chatu potrebna u ER dijagramu
- dogovoreno da ćemo do kraja dana raspraviti o Paypalu ili Stripeu kao servisima za plaćanje koje ćemo koristiti u drugom ciklusu

### Osmi timski sastanak: online koordinacija prije predaje
Datum: 12. studenoga 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- Renee obavijestila tim da ne može prisustvovati zadnjem sastanku ovaj ciklus, dogovoreno da će Mia poslati mail asistentici
- dodatni dogovor oko prirode zahtjeva za donacijama zbog poteškoća u stvaranju ER dijagrama
    - razjašnjeno da će biti jedan aktivan zahtjev po chatu u nekom trenutku
    - dogovoreno da odbijanje zahtjeva ne znači nužno da se ne može opet poslati zahtjev
- dogovoreno da je implementacijski zbog mogućnosti i broja korisnika povijest zahtjeva za donaciju pohranjivati u bazu podatakaa
- finalizirani ER dijagrami
- dokumentacijski tim dogovorio se oko finalizacije UC i sekvencijskih dijagrama do srijede, finalizacija klasnih dijagrama i ostale dokumentacije što prije
- razrađene nejasnoće oko integracijskih testova

### Deveti timski sastanak - sastanak prije praznika
Datum: 19. prosinca 2025.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- tim obaviješten o temama diskutiranima na sastanku s asistenticom i demosom
- riješeni problemi koje su članovi backend i frontend tima imali s lokalnim uređivanjem koda
- dodani lokalni korisnici za lakše ocijenjivanja rada
- dogovorili se o tome da se može ažurirati potreba udruge za vrijeme kampanja, korisnici odabiru što žele donirati i onda kasnije udruge mogu promijeniti to ako nešto donirano nije dobro
- dogovorili se da prvo treba implementirati chat (to uključuje zahtjeve), onda plaćanje i recenzije, zatim kampanje i onda na kraju implementirati uređivanje profila (sort i filter) -> sinkronizirano na GitHub Projectsu
- dogovoreno da frontend treba izraditi dizajn za chat, kampanje, profil, status dostave
- dogovorili se da će biti potreban sastanak backend - frontend nakon što se upoznaju s Stream Chatom

### Deseti timski sastanak - razrada plana do predaje
Datum: 9. siječnja 2026.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- održali smo pregled napravljenog/što treba napraviti do alfa prezentacije i do kraja
- zaključak: trebali smo biti redovitiji u radu -> kako bi to popravili napravili smo detaljniji plan s rokovima oko kojeg smo se složili, dodijelili odgovornosti direktno
- do 16.1. (alfa prezentacija)
    - backend mora zavrsiti chat integraciju
    - započeti stripe integraciju
    - frontend tim treba napraviti dizajn za kampanje
    - napraviti lokalne račune i ugraditi mogućnost za njihovu izradu (zadužen Domagoj)
    - završiti chat integraciju do 14.1 (zadužen backend tim)
    - započeti Stripe integraciju do 13.1 (zadužen Domagoj)
    - razraditi recenzije (zadužen backend tim)
    - 15.1. održati brzi online sastanak i izvršiti deploy
    - do 16.1. napraviti automatska testiranja (zadužen docs tim)

- do završne predaje (23.1.) 
    - 19.1. 23.59 je zamrzavanje značajki ("feature freeze) (treba napraviti recenzije + kampanje)
    - gotovo plaćanje
    - napravljen filter/sort oglasa po parametrima
    - dovršiti sve vezano uz profil (uređivanje)
    - napraviti generalno čišćenje koda od 21.1. nadalje
    - završiti razvitak dijagrama komponenti i razreda (docs tim koordinirati s backend timom sukladno razvoju)
    - izraditi prezentaciju
- 30.1 je usmena obrana, dogovoreno da ćemo individualno nakon predaje detaljno prolaziti kroz tuđi kod, održavati online sastanke tijekom tog zadnjeg tjedna navečer

### Jedanaesti sastanak - kratka koordinacija nakon alfa prezentacije
Datum: 16. siječnja 2026.

Prisustvovali: M.Malović, I.Džepina, D.Gavranić, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- velikom većinom smo pratili plan i implementirali većinu onog što je planirano prethodni sastanak
    - testiranja će zbog implementacije morati biti pomaknuta kasnije u zadnji tjedan
- potrebno još zadnji tjedan dovršiti plaćanje i recenzije i popraviti bugove koji su nam postali očiti i obaviti što treba zadnji tjedan

### Dvanaesti sastanak - koordinacija prije završne predaje
Datum: 22. siječnja 2026.

Prisustvovali: M.Malović, I.Džepina, R.Gulan, V.Milanović, V.Ružić, D.Žic
Teme sastanka:
- dogovorili se kako će izgledati završna prezentacija i što ćemo u skladu sa smjernicama u nju uključiti, odabrali dizajn iste
- uočili i popravili bug vezan uz kampanje (kad igračke imaju ista imena), popravili i pushali promjene
- sagledali obavljen posao: još potrebno objaviti neke UML dijagrame i dovršiti testiranja


# Tablica aktivnosti


Ispod u tablici navodimo koliko je sati koja osoba uložila u pojedinu komponentu projekta.

| Aktivnost | M.Malović | I.Džepina | D.Gavranić | R.Gulan | V.Milanović | V.Ružić | D.Žic |
|---|---:|---:|---:|---:|---:|---:|---:|
| Upravljanje projektom | 12 |  |  |  |  |  |  |
| Opis projektnog zadatka | 3 | 2 |  |  |  |  |  |
| Funkcionalni zahtjevi | 2 | 6 | 1 | 1 | 1 | 1 | 1 |
| Opis pojedinih obrazaca | 8 | 10 |  |  |  |  |  |
| Dijagram obrazaca | 12 | 21 |  |  |  |  |  |
| Sekvencijski dijagrami | 8 |  |  |  |  |  |  |
| Opis ostalih zahtjeva |  | 6 |  |  |  |  |  |
| Arhitektura i dizajn sustava |  |  | 25 | 24 | 20 | 11 | 12 |
| Model baze podataka |  |  | 4 |  |  |  | 2 |
| Dijagram razreda | 1 |  | 2 |  |  | 5 |  |
| Dijagram stanja |  | 3 |  |  |  |  |  |
| Dijagram aktivnosti | 2 |  |  |  |  |  |  |
| Dijagram komponenti | 5 |  |  |  |  |  |  |
| Dijagram razmještaja |  | 2 |  |  |  |  |  |
| Korištene tehnologije i alati | 1 |  | 1 |  |  | 1 | 1 |
| Ispitivanje programskog rješenja | 10 | 18 | 8 | 11 | 14 | 5 | 5 |
| Upute za puštanje u pogon |  |  | 3 |  |  |  |  |
| Dokumentacija - razno | 15 | 13 | 1 |  |  |  | 1 |
| Izrada FE dijela aplikacije |  |  | 40 | 63 | 51 |  |  |
| Izrada BE dijela aplikacije |  |  | 26 |  |  | 60 | 76 |
| Deployment |  |  | 8 |  |  |  |  |
| Izrada baze podataka |  |  |  |  |  | 2 | 3 |
| Izrada prezentacije | 1 | 4 |  |  |  |  |  |
| Sudjelovanje na sastancima | 20 | 11 | 11 | 12 | 13 | 11 | 14



# Dijagram pregleda promjena 

Prenijeti dijagram pregleda promjena nad datotekama projekta. Potrebno je na kraju
projekta generirane grafove s githuba prenijeti u ovo poglavlje dokumentacije. Dijagrami
za vlastiti projekt se mogu preuzeti s github.com stranice, u izborniku Repository, pritiskom
na stavku Contributors.

# Ključni izazovi i rješenja
### Zaključak rada
Općenito smo zadovoljni cijelim projektom. Postigli smo ono što smo htjeli na početku semestra. Tim je bio koherentan i dobrog raspoloženja te složno funkcionirao.
### Opisi glavnih izazova
- relativno malo znanje cijelog tima o tehnologijama potrebnima za izradu i dokumentaciju moderne web aplikacije
- izazovi u međusobnoj komunikaciji 
    - nejasna podjela rada koja završava tako da se nešto napravi dvaput ili nijednom
    - nejasno definiranje rokova i odgovornosti koja uzrokuje nepoštivanje rokova
    - poteškoće vezane uz pravovremeno obavještavanje članova tima vezano uz obavljene poslove, odgovore na pitanja prema asistentici i sl.
### Rješavanje izazova, naučene lekcije
- problem nedovoljnog poznavanja tehnologija riješili smo tako da su članovi tima koji su upoznati s nekim tehnologijama dijelili svoje znanje onima koji nisu toliko upoznati te tako da smo se međusobno poticali da što više (pogotovo na početku) zajedno i pojedinačno učimo i istražujemo o potrebnim tehnologijama i programima
- pokušavali smo nejasnoće i probleme vezane uz razumijevanje nekih svojstava rješavati zajedno.
- na sastancima smo pokušavali što jasnije definirati tko je zadužen za koji dio posla i do kad očekujemo da nešto bude gotovo
- u drugom ciklusu pokušali smo i unutar timova jasnije dodijeliti tko je zadužen za što kako bi izbjegli nesporazume
- pokušavali smo pratiti tko radi što u nekom tjednu tako da znamo tko je trebao nešto napraviti kako bi znali da smo dobili odgovor na neko pitanje ili da je neki posao napravljen iako još možda nije objavljen na GitHub ili na Notion

- naučene lekcije: podijeliti odgovornosti na vrijeme i detaljno, napraviti svoj dio posla na vrijeme i na vrijeme komunicirati da je obavljen ili ako je bilo problema s obavljanjem istog



