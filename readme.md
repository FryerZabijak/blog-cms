# Blog CMS s administrací

## Instalace

1. Stáhněte si nebo naklonujte tento repozitář
2. Nainstalovat Python
3. Nainstalovat NodeJs
4. Nainstalovat knihovny:
`pip install Flask`
`pip install flask_sqlalchemy`
`pip install flask_login`
5. Spusťte server pomocí `flask run` (pro debug přidejte `--debug`)
Na Windowsu může dělat problém, kdyžtak spustit pomocí `python -m flask run`

### Styly

1. Spusťte watch Tailwind CSS stylů pomocí `npx tailwindcss -i ./static/css/style.css -o ./static/css/output.css --watch`
Pozn. Tailwind se neimportuje celý najednou, ale přidává pouze ty styly, které jsou potřeba. Proto takhle bude sledovat třídy v souborech, které si nastavíte v `tailwind.config.js`

## Funkce

- Přidávání, úprava a mazání článků
- Přidávání, úprava a mazání uživatelů (pouze pro administrátory)
- Přihlašování a odhlašování

## Technologie

- Python
- Flask
- Jinja
- HTML
- SQLAlchemy
- TailwindCSS
- CSS
- JS

## Licence

Projekt je licencován pod [MIT Licencí]

