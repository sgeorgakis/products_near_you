Products Near You
=================

The purpose of this exercise is to build an API that returns the most popular products
from shops near you.

Provided goodies
----------------

1. A server boilerplate using `Flask`. To run the server:

  ```
  $ python runserver.py
  ```

2. A rudimentary client so you can visualize the results more easily. The client does not
have any way to communicate with the API so you will need to implement that. To run the
client:

  ```
  $ cd client
  $ python -m SimpleHTTPServer
  ```

3. Four datasets in CSV format:
    * `shops.csv`: shops with their coordinates
    * `products.csv`: products per shop along available quantity and global popularity
    * `tags.csv`: a bunch of tags
    * `taggings.csv`: what tags each shop has

What you need to do
-------------------

1. Create a Python virtualenv and install the requirements:

    ```
    $ pip install virtualenvwrapper
    $ mkvirtualenv
    $ pip install -r requirements.txt
    ```

2. Implement the `Searcher.search()` method in the client so it can communicate with your
API. We've included `jQuery` on the page so you can use that if you like.

3. Build the `/search` endpoint which returns the N most popular products across all shops
near the user. The endpoint should receive:
    1. the number (N) of products to return
    2. a pair of coordinates (the user position)
    3. a search radius (how far the search should extend)
    4. optionally, some tags (what types of shops the user wants to see)

    If tags are provided, a shop needs to have at least one of them to be considered a
    candidate. You can use any Python library to your aid but you can't use any external
    databases or search engines (e.g PostGIS, Elasticsearch, etc). You should build your
    solution as if the data is static and cannot be updated by any external processes.

4. Write some tests. A test foundation is provided for you in `tests/conftest.py`.

5. Briefly think about and answer the questions in THOUGHTS.md.

*You should deliver your solution as a `git` repository, preferably hosted on GitHub.*

Things we look for
------------------

In a nutshell we're looking for correctness, good code design and sensible choices when
it comes to performance. Imagine that your API will be used by a lot of people – how does
that affect your design? Also, imagine that your code will be read by other developers in
your team – keep them happy :-)

Resources
---------

1. `Flask`: http://flask.pocoo.org/
2. `pytest`: http://pytest.org/latest/
3. `virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/


Solution Notes
=================

The project uses the Flask framework to create an application.
First, the data are loaded from the csv files in a suitable data structure.
After that, the application is ready to handle requests.
**CORS is enabled for all origins.**

The request should use the `GET` HTTP method and pass all the arguments as query parameters.
A valid request url has the following format:

`/search?count=10&radius=500&lat=59.33258&lng=18.0649&tags=home,shirts`

The `count` parameter is the number of products to be returned and must be an integer.

The `radius` parameter is the search radius of shops in meters and must be an integer.

The `lat` parameter is the latitude of the user's position and must be a float.

The `lng` parameter is the longitute of the user's position and must be a float.

The `tags` (optional) parameter are the tags that the shop must have at least one and is a string
with values separated by commas.

If any of the above parameters is invalid, a `Bad Request` response is returned,
holding the a message with the wrong parameter in its body in JSON format.

The application uses the [Vincenty's formulae](https://en.wikipedia.org/wiki/Vincenty%27s_formulae)
to calculate the distance of the user's coordinates with the ones of a shop and check if it is within the search radius.
After all the matching products are found, they are reversed sorted by popularity
and the N first are returned where N the `count` parameter specified in the request.

Known Issues
------------

In the front end app, according to jQuery's documentation and various resources,
the response message in case of an error should be found in response object's `responseJSON` attribute.
While testing this functionality, the `responseJSON` attribute was always null,
although the response from the server was the expected one.
This does not allow the user to be presented the error message returned.

Thoughts
------------

In the back end app, the products are hold in a set.
That means that all the products within matching shops must be selected
and then sorted by popularity, adding some delay.
An initial thought was to hold the products within a list
and sort them by popularity within the function that holds the data.
After that, while filtering the products, if the desired number is reached,
the filtering should stop and the products already passed the filtering should be returned.
While trying to implement the above, I found out that the initial sorting
took much longer than expected, so I decided not to follow that idea.

It turned out that the filtered products were not so many to add much delay in the sorting
and I implemented this approach.
