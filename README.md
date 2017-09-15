# Gender Ratio Calculator for Facebook Events (Python)
fbratio.py is a small Python script that pulls guest information for a Facebook event, and then determines their gender using first names through calls to the [Genderize.io API](https://genderize.io/).
## Installation
* Make sure you have the latest version of [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) installed.
* Install the [Facebook SDK for Python](http://facebook-sdk.readthedocs.io/en/latest/install.html#installing-from-git) under a virtualenv.
## Running the Program
### Getting a User Access Token
1. Go to Facebook for Developer's [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. On the top right of the Graph API Explorer, click on Get Token -> Get User Access Token.
3. Check "user_events" under Events, Groups & Pages.
4. Click Get Access Token; Facebook will request the appropriate permissions. **Facebook needs permissions to retrieve information from the Graph API**.
5. The User Access Token will appear in the textbox located in the top, *copy the token* and save for later.
### Executing the Script
In a terminal window, run the ratio.py with the following line.
~~~python
python fbratio.py
~~~
The program will then ask for the User Access Token and Facebook event identifier. You can get the Facebook event ID from the event URL.
~~~
https://www.facebook.com/events/(EventID)/
~~~
### Command Line Arguments
* -hc: Runs the hardcoded token and event in the header of fbratio.py
* -i [token] [eventid]: Runs the inline arguments instead of prompting
* -g: Prints the names of all guests.
* -n: No call to the Genderize.io API
