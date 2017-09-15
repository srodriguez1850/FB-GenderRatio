# FB-GenderRatio
## Installation
* Make sure you have the latest version of [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) installed.
* Install the [Facebook SDK for Python](http://facebook-sdk.readthedocs.io/en/latest/install.html#installing-from-git) under a virtualenv.
## Running the Program
### Getting a User Access Token
1. Go to Facebook for Developer's [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. On the top right of the Graph API Explorer, click on Get Token -> Get User Access Token.
3. If the event is owned by a page, check "manage_pages" and "pages_show_list" under Events, Groups & Pages.
4. Click Get Access Token; Facebook will request the appropriate permissions (profile information, events, pages). **Facebook needs permissions to make the correct calls to the Graph API**.
5. The User Access Token will appear in the textbox located in the top, *copy the token* and save for later.
### Executing the Script
In a terminal window, run the ratio.py with the following line.
~~~python
python ratio.py
~~~
The program will then ask for the User Access Token and Facebook event identifier. You can get the Facebook event ID from the event URL.
~~~
https://www.facebook.com/events/(EventID)/
~~~
### Command Line Arguments
* -h: Runs the hardcoded token and event in the header of ratio.py
* -i [token] [eventid]: Runs the inline arguments instead of prompting.
* -g: Prints the names of all guests.
