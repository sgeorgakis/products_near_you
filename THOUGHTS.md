1. How would your design change if the data was not static (i.e updated frequently
during the day)?

If the data was not static, the usage of a database is necessary.
Loading the data is an expensive operation.
Filtering the products to match the request's arguments would take place in the database level,
making the request handling faster.
A database would also allow the application to handle much bigger size of data.
Moreover, the application could always use a caching layer to hold some of (if not all)
the data in memory and increase speed.
The main problem with this approach is to determine when to update the cache.
This has to do with the way the data are updated.
If for example, they are updated in a fixed interval, then the cache can be invalidated in the same interval.
If the app is also responsible for updating the data (through a different endpoint),
then updated data should be invalidated while updating the database.


2. Do you think your design can handle 1000 concurrent requests per second? If not, what
would you change?

According to Flask's documentation, the current design can handle only one request at a time.
Although it is quite easy to make it handle concurrent requests using threads,
I believe that 1000 concurrent cannot still be handled.
The best approach would be to deploy my application in a different WSGI server
(like Gunicorn) that would be able to scale my application.
