from gudlft import create_app

if __name__ == "__main__":
    app = create_app(testing=True)
    if 'SERVER_PORT' in app.config.keys():
        port = app.config['SERVER_PORT']
    else:
        port = 5000
    app.run(host='localhost', port=port)
