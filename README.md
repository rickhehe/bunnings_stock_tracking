# Bunnings Stock Tracking
## Is stock avialability notifier a better name?

## **token** and **clientID** are subject to expiration!

This is another request from an internal customer (AKA the Wife). She is interested in a product which is currently out of stock (at the time of first commit), and she want's to be notified when it is back in stock in any of the Christchurch stores.

Interested products can be defined in the **products.csv**. The record in the file is for demonstration only. It does not have energy monitoring function which means I can track the power consumption.

You will need **HASS** and **AppDaemon** installed and running. Also, you will need to define **token** and **clientID** in the **apps.yaml**.

Also, to uitilize the **E-mail** function, you will need to have the notifier defined in **configuration.ymal**.

Of course, you still need to get that **token** and **clientID** first... This is a bit tricky. I had issues with getting authentication information from the header in a returned response and eventually I copied them from the browser - and it works.

BTW, I was in K...Care once and was supprised that main retailers don't provide any API to share stock moves of their products with them. I am pretty sure they are doing great planning production without this information though.
