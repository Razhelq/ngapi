# ngapi

NGAPI application provides a few endpoints which allow to post/get a movie or comment to the database and display top commented movies.

- POST /movies:
    e.g. /movie
- GET /movies:

POST /comments:

        ​Request body should contain ID of movie already present in database, and comment text body.
        Comment should be saved to application database and returned in request response.

GET /comments:

        ​Should fetch list of all comments present in application database.
        Should allow filtering comments by associated movie, by passing its ID.

GET /top:

        ​Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
        Movies with the same number of comments should have the same position in the ranking.
        Should require specifying a date range for which statistics should be generated.

Example response:

[

    {

        "movie_id": 2,

        "total_comments": 4,

        "rank": 1

    },

    {

        "movie_id": 3,

        "total_comments": 2,

        "rank": 2

    },

    {

        "movie_id": 4,

        "total_comments": 2,

        "rank": 2

    },

    {

        "movie_id": 1,

        "total_comments": 0,

        "rank": 3

    }

]


Rules & hints

    ​Your goal is to implement REST API in Django, however you're free to use any third-party libraries and database of your choice, but please share your reasoning behind choosing them.
    At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
    The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
    Please dockerize your application and use docker-compose or similar solution.
    Written application must be hosted and publicly available for us online - we recommend Heroku.
2015-02-11T00:00:00.000Z
GET /top/?date_start=2020-04-17T00:00:00.000Z&date_end=2020-04-19T00:00:00.000Z