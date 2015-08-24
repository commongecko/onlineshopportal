# onlineshopportal

## ER diagram
http://i.imgur.com/jy3XSpi.png

## Login Credentials
#### Admin superuser
    user: admin
    pass: abc

#### Seller user with item modify/add/delete permissions
    user: seller1
    pass: seller1

#### Customer user
    user: user
    pass: user

    user: user2
    pass: user2


Problem statement:
This is a online shopping portal application with basic functionlities. The app has two types of users- admin and customers. Admin manages the app (adding items, discounts and modifying user profiles)  and customers use the app to shop online. App should have following features implemented.

    Phase -I
        Features to Include:
                Admin
                    Adding/Editing/Deleting Items:Create a Item table to add following data related to it. Kindly choose correct data type for each db table field.
                        Item Name
                        Item Cost
                        Item Discount
                        Available number
                    Keep one default Customer, one default Item for phase-I
                Customer
                    Customers should be able to see Items available.
                    Customers should be able to buy any of the available items.
                    Customers should be able to view items in basket, quantity purchased, discounted individual price for the item and final price for number of items being brought, total bill amount anytime they want.
                    Store every transaction with date and time for future reference.
                Steps:
                    Design the database tables.
                    Implement the UI, get the UI reviewed.
                    Write views and connect them using urls.
    Phase -II:
            Design a login page where only Admin approved users can login
            Features to add:
                admin
                    Adding/Editing/Deleting Customers
                    Create a Customer table to add following data related to it
                        Customer name
                        Customer ID
                        Customer description
                Every Customer should have two baskets, Wishlist and checkout.
            Customer
                Customers should be able to see their baskets anytime they want.
                Customers should be able to add items to any of the basket.
            Steps:
                Use django user login module
    Phase-III:
            Features to add:
                admin
                    Adding/Editing/Deleting Sellers
                    Add Seller field to Item table
                Seller
                    Adding/Editing/Deleting Items
                Should be able to view all transactions of items sold.
            Steps
                Design the database tables.
                Implement the UI, get the UI reviewed.
                Write views and connect them using urls.


