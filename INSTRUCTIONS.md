# Upute za instalaciju i pokretanje

> Ovaj dokument pruža detaljne smjernice za instalaciju, konfiguraciju, pokretanje i administraciju PlayForward aplikacije. Aplikacija se sastoji od Django backend servisa i Vue.js frontend aplikacije, te koristi PostgreSQL bazu podataka.

## Sadržaj
- [1. Razvojno okruženje (lokalno)](#1-razvojno-okruženje-lokalno)
- [2. Produkcijsko okruženje (Digital Ocean Droplet)](#2-produkcijsko-okruženje-digital-ocean)
- [3. Administracija aplikacije](#3-administracija-aplikacije)

---

## 1. Razvojno okruženje (lokalno)

### 1.1 Preduvjeti

Za lokalni razvoj potrebno je instalirati sljedeći softver:

- **Python 3.13+** i **pip**
- **Node.js 20.19+ ili 22.12+**
- **Git**

Koriste se i sljedeći package manageri (ako ih nemate instalirane, slijedite upute u nastavku):
- **pnpm**
- **uv**

### 1.2 Preuzimanje projekta

Klonirajte Git repozitorij:

```bash
git clone https://github.com/maucikamau/PROGI-G1.3.git
cd PROGI-G1.3
```

### 1.3 Postavljanje backend servisa

1. Instalirajte `uv` ako ga nemate:
```bash
pip install uv
```

2. Kreirajte virtualno okruženje i instalirajte Python ovisnosti:
```bash
cd backend
uv venv -p 3.13
source .venv/bin/activate
uv sync
```

3. Napravite `.env` datoteku za razvojno okruženje:
```bash
touch .env
cp .env.example .env
```

Postavite potrebne varijable u `.env` datoteci.
Potrebni su:
- [Stripe račun](https://stripe.com/docs/keys)
- [StreamChat račun](https://getstream.io/chat/docs/)

kako bi vam sve mogućnosti radile kako treba. Slijedite upute za dobivanje API ključeva.

4. Pokrenite migracije za bazu podataka:
```bash
uv run python manage.py migrate
```

5. Napravite superuser račun za pristup admin sučelju:
```bash
uv run python manage.py createsuperuser
```

6. Pokrenite web server:
```bash
uv run python manage.py runserver
```

Backend će biti dostupan na `http://localhost:8000`

### 1.4 Postavljanje frontend aplikacije

1. Instalirajte `pnpm` globalno ako ga nemate:
```bash
npm install -g pnpm
```

2. Pozicionirajte se u frontend direktorij:
```bash
cd ../frontend
```

3. Instalirajte potrebne pakete:
```bash
pnpm install
```

4. Pokrenite razvojni server:
```bash
pnpm run dev
```

Frontend će biti dostupan na `http://localhost:5173` (ili drugi port koji Vite odabere).

### 1.5 Testiranje

**Backend testovi:**
```bash
cd backend
uv run pytest
```

---

## 2. Produkcijsko okruženje [Digital Ocean]

### 2.1 Preduvjeti

Za produkcijsko okruženje potreban je:

- **Ubuntu 25.04** server (Digital Ocean Droplet ili drugi VPS)
- **Minimalno 1GB RAM** (preporučeno 2-4GB)
- **20GB prostora** na disku
- **SSH pristup** serveru s root ili sudo ovlastima
- **Domena** (u našem slučaju: `playforward.dedyn.io`)

### 2.2 Priprema servera

Ažurirajte sustav:

```bash
apt update && apt upgrade -y
```

### 2.3 Instalacija Docker-a i Docker Compose-a

1. Instalirajte potrebne pakete:
```bash
apt install -y ca-certificates curl gnupg lsb-release git
```

2. Dodajte Docker GPG ključ:
```bash
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
```

3. Dodajte Docker repozitorij:
```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

4. Instalirajte Docker:
```bash
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

5. Provjerite instalaciju:
```bash
docker --version
docker compose version
```

6. Omogućite Docker da se pokreće pri boot-u:
```bash
systemctl enable docker
systemctl start docker
```

### 2.4 Kreiranje non-root korisnika s Docker pravima (PREPORUČENO)

Iz sigurnosnih razloga, preporučuje se kreirati posebnog korisnika umjesto korištenja root računa.

1. Kreirajte novog korisnika (npr. `playforward`):
```bash
adduser playforward
```

Sustav će vas pitati za lozinku i dodatne informacije. Unesite sigurnu lozinku.

2. Dodajte korisnika u `docker` grupu kako bi mogao izvršavati Docker naredbe bez `sudo`:
```bash
usermod -aG docker playforward
```

3. Kreirajte direktorij za aplikaciju i dodijelite vlasništvo novom korisniku:
```bash
mkdir -p /opt/playforward
chown -R playforward:playforward /opt/playforward
```

4. Prijeđite na novog korisnika:
```bash
su - playforward
```

5. Testirajte Docker pristup:
```bash
docker ps
docker --version
```

### 2.5 Preuzimanje projekta

1. Pozicionirajte se u direktorij aplikacije:
```bash
cd /opt/playforward
```

2. Klonirajte repozitorij:
```bash
git clone https://github.com/maucikamau/PROGI-G1.3.git .
```

### 2.6 Konfiguracija produkcijskog okruženja

1. Pozicionirajte se u produkcijski direktorij:
```bash
cd /opt/playforward/deployment/prod
```

2. Kreirajte Docker mrežu:
```bash
docker network create playforward
```

3. Kopirajte primjer `.env` datoteke:
```bash
cp .env.example .env
```

4. Uredite `.env` datoteku:
```bash
nano .env
```

Popunite sljedeće varijable:

```dotenv
POSTGRES_DB=playforward-prod
POSTGRES_USER=playforward_user
POSTGRES_PASSWORD=GENERIRAJ_SIGURAN_PASSWORD
DATABASE_URL=postgresql://playforward_user:GENERIRAJ_SIGURAN_PASSWORD@prod-db:5432/playforward-prod
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@playforward.dedyn.io
DJANGO_SUPERUSER_PASSWORD=GENERIRAJ_SIGURAN_ADMIN_PASSWORD
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY="GENERIRAJ_RANDOM_STRING_50_ZNAKOVA"
DJANGO_ALLOWED_HOSTS=playforward.dedyn.io,localhost
DJANGO_DEBUG=false
```

**Važno:** 
- Za generiranje sigurnog `DJANGO_SECRET_KEY`, koristite: 
  ```bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Koristite jake lozinke za `POSTGRES_PASSWORD` i `DJANGO_SUPERUSER_PASSWORD`

5. Dodajte API ključeve za StreamChat i Stripe. Kreirajte `/opt/playforward/backend/.env`:
```bash
nano .env
```

Dodajte sljedeće (koristite vaše stvarne ključeve):
```dotenv
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

STREAM_API_KEY=your_stream_api_key
STREAM_API_SECRET=your_stream_api_secret
```

### 2.7 Pokretanje aplikacije

1. Pripremite docker image:
```bash
cd /opt/playforward/deployment/prod
docker compose pull
```

2. Pokrenite kontejnere:
```bash
docker compose up -d
```

3. Provjerite status kontejnera:
```bash
docker compose ps
```

Trebali biste vidjeti dva servisa (`web` i `prod-db`) u statusu "running".

4. Provjerite logove:
```bash
docker compose logs -f web
```

Pritisnite `Ctrl+C` za izlaz iz prikaza logova.

### 2.8 Postavljanje Nginx reverse proxy-ja u Docker kontejneru (PREPORUČENO)

Nginx će se pokretati u zasebnom Docker kontejneru koji dijeli istu `playforward` mrežu s aplikacijom.

#### 2.8.1 Priprema Nginx konfiguracije

1. Pronađite dostupnu nginx konfiguraciju:
```bash
cd /opt/playforward/deployment/nginx
```

2. Provjerite da postoje potrebne datoteke:
```bash
ls -la
```

Trebali biste vidjeti:
- `docker-compose.yaml`
- `nginx.conf`
- `conf.d/playforward-http.conf` (za HTTP)
- `conf.d/playforward.conf` (za HTTPS, koristit će se nakon SSL certifikata)

3. Privremeno preimenujte HTTPS konfiguraciju (koristit ćemo je kasnije):
```bash
mv conf.d/playforward.conf conf.d/playforward.conf.disabled
```

#### 2.8.2 Pokretanje Nginx kontejnera

1. Pokrenite Nginx kontejner:
```bash
docker compose up -d
```

2. Provjerite status:
```bash
docker compose ps
```

3. Provjerite logove:
```bash
docker compose logs nginx
```

4. Testirajte pristup aplikaciji (morate postaviti domenu da prikazuje na ovaj server):
```bash
curl -I http://playforward.dedyn.io
```

Trebali biste dobiti HTTP 200 odgovor.
Ukoliko dobijete HTTP_HOST grešku, provjerite jeste li u DJANGO_ALLOWED_HOSTS postavili domenu odnosno IP adresu.

#### 2.8.3 Postavljanje SSL certifikata s Let's Encrypt

1. Pokrenite Certbot za dobivanje SSL certifikata:
```bash
docker compose run --rm certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    -d playforward.dedyn.io \
    --email <<VAŠ_EMAIL>> \
    --agree-tos \
    --no-eff-email
```

2. Provjerite da je certifikat uspješno kreiran:
```bash
docker compose exec nginx ls -la /etc/letsencrypt/live/playforward.dedyn.io/
```

Trebali biste vidjeti `fullchain.pem` i `privkey.pem`.

#### 2.8.4 Aktivacija HTTPS konfiguracije

1. Deaktivirajte HTTP konfiguraciju i aktivirajte HTTPS:
```bash
mv conf.d/playforward-http.conf conf.d/playforward-http.conf.disabled
mv conf.d/playforward.conf.disabled conf.d/playforward.conf
```

2. Ponovno učitajte Nginx konfiguraciju:
```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

Ili jednostavno restartajte kontejner:
```bash
docker compose restart nginx
```

3. Testirajte HTTPS pristup:
```bash
curl -I https://playforward.dedyn.io
```

Za ručno obnavljanje certifikata:
```bash
docker compose run --rm certbot renew
docker compose exec nginx nginx -s reload
```

### 2.9 Provjera rada aplikacije

Otvorite web preglednik i posjetite:
- **Glavna aplikacija**: `https://playforward.dedyn.io`
- **Admin panel**: `https://playforward.dedyn.io/admin/` (važan je / na kraju)

Prijavite se na admin panel s kredencijalima koje ste postavili u `.env` datoteci.

---

## 3. Administracija aplikacije

### 3.1 Pristup administratorskom sučelju

**URL**: `https://playforward.dedyn.io/admin/`

Koristite superuser račun koje ste definirali pri postavljanju (`DJANGO_SUPERUSER_USERNAME` i `DJANGO_SUPERUSER_PASSWORD`).

### 3.2 Ažuriranje aplikacije

Kada želite napraviti deploy nove verzije aplikacije:

```bash
cd /opt/playforward/deployment/prod

docker compose pull
docker compose up -d
docker compose logs -f web
```

### 3.3 Pregled logova

#### Logovi Docker kontejnera

Pregled logova web servisa:
```bash
cd /opt/playforward/deployment/prod
docker compose logs web
```

Pregled logova u stvarnom vremenu:
```bash
docker compose logs -f web
```

Pregled logova baze podataka:
```bash
docker compose logs prod-db
```

#### Logovi Nginx-a

```bash
cd /opt/playforward/deployment/nginx

# Access i error logs
docker compose logs nginx

# U stvarnom vremenu
docker compose logs -f nginx
```

### 3.4 Rješavanje problema

#### Kontejner se ne pokreće

1. Provjerite status:
```bash
docker compose ps
```

2. Pregledajte logove:
```bash
docker compose logs web
docker compose logs prod-db
```

3. Provjerite `.env` konfiguraciju:
```bash
cat .env
```

4. Ponovno pokrenite kontejnere:
```bash
docker compose down
docker compose up -d --force-recreate
```

#### Baza podataka nije dostupna

```bash
# Provjerite je li PostgreSQL kontejner pokrenut
docker compose ps prod-db

# Provjerite health status
docker compose exec prod-db pg_isready -U playforward_user

# Restart baze podataka
docker compose restart prod-db
```

#### Aplikacija ne odgovara

Pokušajte ponovno pokrenuti kontenjere.
```bash
docker compose down
docker compose up -d
```


#### Više o Docker debugging-u:
- [Docker dokumentacija - Pregled logova](https://docs.docker.com/config/containers/logging/)
- [Docker Compose troubleshooting](https://docs.docker.com/compose/troubleshooting/)

### 3.6 Sigurnosne preporuke

1. **Firewall**

Omogućite samo potrebne portove:
```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

---

## 4. Opis pristupa aplikaciji na javnom poslužitelju

### 4.1 Pristup za korisnike

Aplikacija je dostupna na adresi: **https://playforward.dedyn.io**

Korisnici mogu:
- Pregledavati dostupne igračke
- Registrirati se i prijaviti se
- Objavljivati svoje igračke za donaciju
- Tražiti igračke za svoje dijete ili udrugu
- Koristiti chat funkcionalnost
- Pregledavati i kreirati kampanje

Otvoreni su sljedeći računi za jednostavan pristup funkcionalnostima:

| Vrsta računa       | E-mail                         | Lozinka           |
|--------------------|--------------------------------|-------------------|
| Donator            | donor@playforward.dedyn.io     | 2026donori        |
| Privatni primatelj | primatelj@playforward.dedyn.io | 2026primatelji    |
| Udruga             | udruga@playforward.dedyn.io    | 2026udruge        |
| Administrator      | manager@playforward.dedyn.io   | #pf#manager#2026  |

### 4.2 Pristup za administratore

**Admin panel**: https://playforward.dedyn.io/admin.

Administratori mogu upravljati svim aspektima aplikacije kroz Django admin sučelje.

---

## 5. Dodatni resursi

- **Docker dokumentacija**: https://docs.docker.com/
- **PostgreSQL dokumentacija**: https://www.postgresql.org/docs/
- **Nginx dokumentacija**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/
