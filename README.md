This repository contains the membership register of DOT, Digital Media Club of Aalto University (http://dot.ayy.fi).

Code is partly messy and doesn't always adhere to good design practices. The goal was to complete this project fast and make something that works better than paper or Google docs, so don't be surprised if you find some dirty corners here :-)

If I have time (or interest), I might one day separate the core code from data to form an easily modifiable app that other associations could easily customize for their own use, but I don't see that happening in the very near future...

However, If you are in a need of a simple membership registry and know Django, then this code should work as a base for your own implementation.

Features
--------

Maybe a full list of features?

* configurable annual membership fee
* self-registration of new members
  * confirmation of identity via email
  * automatic invoice creation based on the current fee
  * welcome emails
* easy membership status check / edit mechanism for old members
  * query membership data and short-term edit link via email
  * edit all membership data
  * see full membership status history with invoicing details
  * change e-mail address (requires verification of the new address)
* billing
  * management command to invoice all existing members
  * members get email notification when invoice is marked as paid 
* admin
  * full integration of all models into admin for easy modifications
  * fully versioned data, all changes tracked using django-reversion
