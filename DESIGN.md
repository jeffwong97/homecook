HomeCook by Jeffrey Wong

HomeCook is entirely based within the CS50 IDE. It uses the Flask web framework to enable dynamic web pages
that show relevant recipes to users. It is a Python based website, and uses HTML and CSS for design elements.
It references a SQL database using SQLite, and it uses the CS50 SQL functions to execute database commands
within its Python code. Some low level elements of the logistical framework were taken from my implementation
of CS50 Finance's code, such as the session cookies, error messages, and the login requirement function. The
front-end framework is based on BootStrap v.4.5.3 supplemented by my own CSS file.

The HomeCook database includes a 'recipes' table that includes columns for the recipe id, name, ease of prep,
dish type, and prep time. The 'food' table includes columns for the id and name of each individual food item.
The 'ingredients' table uses two foreign keys to link between the food id and recipe id. The 'users' table
has columns for user id, username, and a hash of their password. The 'saved' table uses two foreign keys to
link between user id and recipe id.

The biggest challenge while implementing this project was working with the database. It was incredibly difficult
to find a recipe database that was open source and free to use, while also providing a large amount of quality
data that is organized well. There were some much larger and more thorough databases containing more information
that would have been very helpful, but they were prohibitive in cost and/or access. As a result I compromised with
a smaller CSV file that was not very well organized. I ended up spending a massive amount of time basically
rebuilding the SQL database after importing it, separating the recipes and their ingredients into different tables
so they can be more easily cross-referenced, filling in data, and narrowing my dataset even more because I had to
delete many entries that simply were nowhere near complete. As a result, the recipe database is nowhere near as big
as I would have hoped to be, and I opted to exclude some basic ingredients such as salt and pepper as well as pictures
of the recipes to be better able to manage the workload during development. If I were to commercialize this product,
however, I would definitely switch over to a larger database.

However, I'm still finding this website to be useful in my daily life as it has cut down on the stress of figuring out
what to cook for dinner, especially in a time where dining out is not really an option at all and grocery stores aren't
always well stocked.