import sys
from gudlft import create_app

if __name__ == "__main__":
    if "real" in sys.argv:
        app = create_app(testing=False)
    else:
        app = create_app()
    if 'PORT' in app.config.keys():
        port = app.config['PORT']
    else:
        port = 5000
    app.run(host='localhost', port=port)
