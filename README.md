# The-Market
An e-commerce web application using Flask, HTML and CSS
## Navigating the file system: 
   - :open_file_folder: **Projects** : root folder for game app
      -  :open_file_folder: **static/** : Contains static files like image files and CSS files
           -   :open_file_folder: **login.css** : css file for login and register 
           -   There are also image files present here that is loaded in my html files when required. 
      
      -  :open_file_folder: **templates/** : Contains HTML  files 
           - :open_file_folder: **layout.html** : This is the layout html file that other html files inherit from 
           - :open_file_folder: **index.html** : HTML file for the main view for the "/" route 
           - :open_file_folder: **login.html** : HTML for the login view 
           - :open_file_folder: **shop.html** : HTML for different categories 
           - :open_file_folder: **cart.html** : HTML for a user's Shopping Cart
           - :open_file_folder: **signup.html** : HTML for the sighning up view
           - :open_file_folder: **create.html** : HTML for creating a listing (contains form)
           - :open_file_folder: **error.html** : HTML for when an error occues (I used this for just testing purposes)
      
      -  :open_file_folder: **app.py** : Main flask application contains all the Models, views and routes. 
      
      -  :open_file_folder: **site.db** : the sqlite databse file 
