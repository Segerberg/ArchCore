# Development

## Localization

Add a new language
<pre>flask translate init [language-code] </pre>

Update all the languages after making changes
<pre>flask translate update</pre>

Compile all languages after updating the translation files
<pre>flask translate compile</pre>

## Docs
### Commands

* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

### Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        development/  # Subfolders for categories
            index.md  # Other markdown pages, images and other files.
               

## Frontend
ArchCore uses the
 
[Jinja2](https://jinja.palletsprojects.com) template engine together with [htmx](https://htmx.org/) and 
[tailwindcss](https://tailwindcss.com) a combination of tools that sometimes is calles the PyHAT web stack. It stands for Python htmx ASGI Tailwind. 
It allows you to build powerful web  applications using nothing more than... Python, htmx, and Tailwind. Hence eliminating the 
need of supporting complex javascript frameworks.

Furthermore Archore tries follows the principle of [HTML First](https://html-first.com/) which boils down to a number of 
practices: 

* Prefer Vanilla approaches
* Use HTML attributes for styling and behaviour
* Use libraries that leverage HTML attributes
* Avoid Build Steps
* Prefer Naked HTML
* Be View-Source Friendly




