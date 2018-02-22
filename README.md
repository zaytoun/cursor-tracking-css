
### CSS-Only Cursor Tracking

![Demo](static/img/demo.gif "cursor tracking in action")

The goal of this project is evaluate the efficacy of cursor tracking utilizing only CSS. The code in this repo is merely a PoC and is purely for experimental purposes.

### Method

Here I describe the method utilized here to accomplishing some degree of cursor tracking:
	
1) Generate a CSS tracking file by first traversing over the DOM of a target html document, crafting selectors that uniquely select each tag on the page by chaining nth-child selectors

2) Define a unique set of keyframes per tag, mapped over a duration and keyframe count (these can be adjusted). Most importantly, each keyframe makes a request using the `url()` function, passing the selector and current duration of time within the url

3) Initially, set animation-play-state of the elements to `paused` but set to `running` for the pseudo-class hover selector

4) On the backend, process each request by mapping selector -> cursor hover time as well as a list of timestamped events in chronological order.

5) Using all this data, one is able to playback the motion of a cursor across the page with decent accuracy.

### Setup

Install Packages: ` sudo pip install -r requirements.txt`

Or use a virtual environment: 

` virtualenv -p python3 venv `

` source venv/bin/activate `

` pip install -r requirements.txt `



Place target html page in the html directory and name it `index.html`

`python tracker.py html/index.html` will produce a `tracker.css` file in `static/css`

`FLASK_APP=app.py flask run`

Go to http://127.0.0.1:5000/ to see the index.html; move you cursor around to send data to the flask server

After that, go to http://127.0.0.1:5000/results/ to see your actions played back to you.

Whenever you wish to clear you session, just run http://127.0.0.1:5000/clear/
