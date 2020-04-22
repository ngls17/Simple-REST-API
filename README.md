# Simple-REST-API
Basic models:<br />
● User<br />
● Post (always made by a user)<br />

Basic Features:<br />
● user signup<br />
● user login<br />
● post creation<br />
● post like<br />
● post unlike<br />
● analytics about how many likes was made. Example url
/api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated
by day.<br />
● user activity an endpoint which will show when user was login last time and when he mades a last
request to the service.<br />

For token authentication used Flask-JWT
