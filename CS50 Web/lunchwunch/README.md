# CS50 Web Capstone Project

## Short Intro

Dynamic Website for a Restaurant

## About

This project builds a dynamic website for a restaurant. The Backend uses django models for Users, Products, User Carts and Transactions/Purchases. The Front end uses JS for managing user carts, image slider and some automated styling effects.

## Distinctiveness and Complexity

### Distinction

This Project is different form google search clone as that project was only a replica of how google search works and it was somewhat static. This project is a dynamic web app and it is for online orders of a restaurant.

The way it differs from Mail Project is that mail project was for sending, archiving, reading and eplying to mails. Sure it was a dynamic web app that used django models but this project targets a totally different scope. Plus the Mail project was SPA while this capstone project is not.

The way it differs from Network Project is that network project was also a SPA. It also targettted social media messaging, likes and comments. This project s not SPA and it has no concept of commenting or likes.

The way it differs from Wiki project is that Wiki was a encylopedia replica which served information on any topic. This project has nothing clos to this. This project does provide information about deals and meals but it also has additional features like cart systems etc. This is totally different from an encyclopedia replica.

The way it differes form commerce project is that commerce project has auctions, comments and bidding while this project doesnt. And this project has user carts and points earned based on transactions which commerce didnt have.

In general this capstone project is different because it has cart system, user points, responsive and reactive pages. While other projects were just niche presenting only the surface logic, this project digs extra deep into how real world systems behave.

### Complexity

This capstone project is surely more complex then any other cs50w project. That's because this project actually touches how real world systems behave rather than just surface level logic. Plus a cart system and dynamic user points is not as easy as it sounds. 

Cart management requires tracking and managing users carts, plus in case products update the cart state should be isolated form new products otheriwse user can have some issues. Then on order placement cart system also makes the final bill and all the discounting happens there and user gets points as specified. The cart is stored using 2 django models named Cart and CartItem. User gets points as 1% of the total bill they pay.

JS on the front end does two jobs. One it dynamically updates the slider on home page. Two it makes sure that when user is adding items to their carts they donot add negative amount.

The project uses 5 django models: User, Product, Cart, CartItem and Transaction. Product stores information related to products including images and Transaction stores payents made in a blockchain style database.

Transaction record is created by taking all the cartitems from a cart and using their data to create a timestamped transaction record that is permanent. Once a transaction record is created it can nver be deleted nor be modified.

## How To Run The Application

Running the application just requires a command as simple as `python3 manage.py runserver`

## Contents

### Misc

- The Web App has its own login and register pages.
- The app also has its own custom 404 page.

### Home

The Home page contains a simple image slider which uses JS to change images rather than bloating with HTML elements.

### Products and More

There is a store page that features the overall products of the restaurant, each product has its own view page. Plus the app also supports product scavaging via categories.

__Thats's it for the README__