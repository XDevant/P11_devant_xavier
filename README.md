# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file.

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be gudlft: <code> $env:FLASK_APP = "gudlft" </code>.

    - You should now be ready to test the application. In the directory, type either <code>python gud.py</code>  (test mode) or <code>python gud.py real</code> (any purchase will be saved in db). The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files] in the gudlft/JSON directory. In testing however the files in test/JSON will be used by Selenium and Locus. Pytest will use a fake db stored in test/data.py. During all testing, subsequent save/load operations will use the test/Temp directory to keep the test db intact. Restart the test server to reinit it.  
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.
    * bookings.json - dictionary of competitions. Values are lists of dicts with a club as key and the number of places booked in the competition by this club

5. Testing

   For running both test commands successfully, you first need to start a test server via <code>python gud.py</code>. Otherwise the 2 test using selenium will fail (they look for port 8000) and locust will wreck the db.

    * Pytest : <code>pytest -sv --basetemp=test\Temp</code>
    * locust: <code>locust -f "test/Locust performance/locustfile.py"</code>

