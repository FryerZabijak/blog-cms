# Blog s administrací

Tento projekt je implementací blogu s administrací pomocí Python Backend Frameworku Flask a jako CSS Framework používám TailwindCSS.

## Instalace

1. Stáhněte si nebo naklonujte tento repozitář
2. Spusťte server pomocí `flask run` (pro debug přidejte `--debug`)

### Knihovny

1. flask_sqlalchemy
2. flask_login

### Styly

1. Spusťte watch Tailwind CSS stylů pomocí `npx tailwindcss -i ./static/css/style.css -o ./static/css/output.css --watch`

## Funkce

- Přidávání, úprava a mazání článků
- Přidávání, úprava a mazání uživatelů (pouze pro administrátory)
- Přihlašování a odhlašování

## Technologie

- Python
- Flask
- SQLAlchemy
- TailwindCSS

## Licence

Projekt je licencován pod [MIT Licencí]

