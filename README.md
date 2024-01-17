# ArchCore
ArchCore

## Projektstruktur 

## Development 


#### Clear database
<pre>
flask db downgrade base
flask db upgrade
</pre>

The initial directive instructs Flask-Migrate to execute the database migrations in a reverse sequence. Without specifying a particular target for the downgrade command, it reverts one revision at a time. If given the base target, it reverses all migrations until the database reverts to its original state, devoid of any tables.

Conversely, the upgrade command re-executes all migrations in a sequential manner. By default, the target for upgrades is 'head,' representing the most recent migration. This action essentially reinstates the tables that were previously downgraded. It's important to note that database migrations do not retain the existing data within the database. Hence, performing a downgrade followed by an upgrade swiftly clears all table contents.


## Translation
Add a new language
<pre>flask translate init [language-code] </pre>

Update all the languages after making changes
<pre>flask translate update</pre>

Compile all languages after updating the translation files
<pre>flask translate compile</pre>

## Unicode
ⓘ
 📖


## Credits

Icons from [https://uxwing.com](https://uxwing.com)


