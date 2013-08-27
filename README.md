This repo contains the membership register of DOT, Digital Media Club of Aalto University (http://dot.ayy.fi).

The code and data are currently pretty heavily tied together. Therefore the register at it's
current form is pretty hard to adapt for any other use. If I have time (or interest), I might one day separate the code from everything else to form a 
pluggable app that other association could easily use for their own purposes. I don't however
see that happening in the very near future...

If you are in need of a simple membership registry and know Django, then this code should work
as a base for your own implementation.

Features
--------

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
  * management command to invoice all old members
  * members get automated notification when invoice is marked as paid 
* admin
  * full integration of all models into admin for easy modifications
  * fully versioned data, all changes tracked (django-reversion)

