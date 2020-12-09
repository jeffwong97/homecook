HomeCook by Jeffrey Wong

HomeCook is a web-based specialized search engine that uses an included database to search for recipes
according to the ingredients that the user inputs. It lets the user either type in or select from a list of
ingredients, then searches the SQL database for recipes that use those ingredients. The idea is to give users
recipes to cook with what is already in their kitchen. Users can also register for their own accounts and
log in to save their favorite recipes for future reference.

To use HomeCook, upload the project's zip file onto CS50's IDE, and unzip. Change into the HomeCook directory
and execute Flask run in the terminal. Click on the link to access the website.

On the search page (a.k.a. home page) users can either choose any number of items in the checkbox list to search,
or type in anything to search. When typed the user is instructed to separate their items with commas, but no
errors should occur with any standard keyboard input. If no results can be found the website should display a
message and prompt the user to search again. If results are found they are listed vertically, including the recipe's
name with a clickable link to the recipe itself, and extra information such as difficulty, dish type, and prep time
underneath. Links should open in new tabls by default. A 'Save' button under that works in two different ways
depending on whether the user is logged in. Search functions do not require logged in accounts and should provide
the same results whether the ingredients are typed in or selected from the checkbox list. However, when viewing
results without logging in, it should not be possible to save recipes, and the 'save' button underneath each result
should remain grayed out.

To register for an account within HomeCook, click 'Register' on the upper right corner inside the navbar.
Users should be able to choose any username that hasn't already been taken, but their chose passwords need to
fulfill the stated requirements before an account can be created. Passwords are stored in the HomeCook database
and hashed using the Werkzeug security functions. Newly registered users are automatically logged in, and
existing users can click 'Log In' on the upper right corner to log in. Their usernames and password hashes are
checked against the database and will be logged in if a match is found.

Once logged in, users will have the ability to save recipes from their searches. The 'Save' button underneath
each result should become pink; once clicked the user and the recipe will become associated in the 'saved'
table of the database, and the user will be redirected to their list of saved recipes with clickable links
to those recipes. The saved recipes page should only be available to logged in users, if any user that is not
logged in somehow tries to access this page they should be redirected to the search page. The saved recipes page
also includes 'Delete' buttons next to each recipe listing, which when clicked deletes that entry in the 'saved'
table of the database.

The YouTube link for this project is https://youtu.be/nNNtbgLYzKU
