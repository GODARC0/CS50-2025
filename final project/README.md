# DAULATBOX
#### Description:
This is my final project for CS50 2025. The name of my project is Daulatbox, and it is a web application. On this website, users can explore different types of ancient and rare currencies, and I’ve also added my personal collection of some rare Indian currencies.

The first folder in this project is the instance folder. It contains a database named daulatbox.db. This database has two tables for the two types of data that the website collects from users. The first is the suggestion table, which stores the user's name, email, and suggestion. The second is the login table, which stores login information. I used SQLite3 to create and manage this database.

The next folder is static, and it contains two subfolders. One is named coins, and it holds all the images of the coins that are shown on the website. The other important file here is style.css. This is where most of the styling for the website is written. A major part of the styling for index.html and other pages comes from this file. I’ve also used some inline CSS and style tags inside specific HTML files where needed. I used a few libraries like Bootstrap, and also took some design elements from CSS UI sites like uiverse.io.

One of the most important (if not the most important) folder is the templates folder. It contains all the HTML files for the different pages of my website. These include:

base.html
This file has all the repeated code and is used with Jinja to shorten the code for other pages. It includes the navigation bar, the suggestion form, and a footer section where I’ve mentioned the future updates I’m planning for the website. I also used some Bootstrap components and a bit of JavaScript here.

index.html
This page uses the layout from base.html (using Jinja). It includes a header with an intro and greeting, followed by an "Explore" button that scrolls down to other sections. These sections include: "Explore Currency," some featured coins or notes, and a few personal quotes. After that, the base.html layout continues.

daulatbook.html
This page contains the information about coins from around the world and also my personal collection, shown in two different sections. It uses images.html to display coin images in the correct layout with information. I plan to expand this by adding a larger database for coins from different countries — but first, I need to learn how to do that.

contact.html
This page has links to my different social media handles. I didn’t add real links because I prefer to keep my social accounts private. Instead, I’ve added my email and GitHub. I used icons from uiverse.io and styled them using style tags directly in the file.

login.html
A simple login page that also includes a registration option. I tried different ways of switching between login and register views, but this one felt the smoothest. Also, I personally prefer minimalistic design, so I stuck with it.

thank_you.html
A small page that thanks the user for submitting a suggestion through the form.

marketplace.html
This page is only accessible after logging in. I haven’t added much to this page yet because it’s a bit complex for now.

profile.html
This page will also be for logged-in users only. Just like marketplace.html, I’ll be adding features to it in the future.

There’s also a logout feature to let users sign out.

Finally, there's the most important file in the project — app.py. This is the backend of the whole website. I referred to the final problem set “Finance” to understand how to create and define routes properly. I also had to Google a lot of things to figure stuff out. In this file, I’ve used a secret key for extra security and defined all the routes for different pages. I combined SQL and Python here, especially for working with the database.

I also used ChatGPT, especially the CS50 Duck, to help debug and understand some parts of the code better.
