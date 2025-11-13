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
Datum: 31. listopad 2025.

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
Datum: 7. studeni 2025.

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
Datum: 12. studeni 2025.

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
# Tablica aktivnosti

_**Kontinuirano osvježavanje**_

Napomena: Doprinose u aktivnostima treba navesti u satima po članovima grupe po
aktivnosti. Potrebno je navesti koliko je sati koja osoba uložila u pojedinu komponentu, možete oblikovati tablicu ili ispisati za svaku osobu.

* Upravljanje projektom
* Opis projektnog zadatka
* Funkcionalni zahtjevi
* Opis pojedinih obrazaca
* Dijagram obrazaca
* Sekvencijski dijagrami
* Opis ostalih zahtjeva
* Arhitektura i dizajn sustava
* Baza podataka
* Dijagram razreda
* Dijagram stanja
* Dijagram aktivnosti
* Dijagram komponenti
* Korištene tehnologije i alati
* Ispitivanje programskog rješenja
* Dijagram razmještaja
* Upute za puštanje u pogon
* Dnevnik sastajanja
* Zaključak i budući rad
* Popis literature
* Dodatne stavke kako ste podijelili
* izradu aplikacije
* npr. izrada početne stranice
* izrada baze podataka
* spajanje s bazom podataka
* izrada prezentacije


# Dijagram pregleda promjena 

Prenijeti dijagram pregleda promjena nad datotekama projekta. Potrebno je na kraju
projekta generirane grafove s githuba prenijeti u ovo poglavlje dokumentacije. Dijagrami
za vlastiti projekt se mogu preuzeti s github.com stranice, u izborniku Repository, pritiskom
na stavku Contributors.

# Kjučni izazovi i rješenja

* Zaključno
* Opis izazova: Glavni izazovi tijekom projekta (npr. kašnjenje u razvoju, tehnički problemi).
* Rješenja: Način na koji su izazovi riješeni, kao i naučene lekcije koje su doprinijele napretku tima.


