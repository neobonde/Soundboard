# EffectPlayerServer

## Building

### Building database

In the `app/database/` folder execute the `init_db.py` script, this will initialize the database.

```$ python init_db.py ```

### Building the backend

Backend is based on python 3.x, running a flask webserver.   

To install the backend install python env

```$ python -m pip install virtualenv```

Now create a python virtual enviorenment in the root of this project

```$ python -m venv env```

> You can choose your own nave for the virtual environment folder, but only env is ignored in the .gitignore

Now activate the `venv`

```$ source env/bin/activate```

Now lets install the required packages from `requirements.txt`

```$ pip install -r requirements.txt ```

And that is it the backend requrements has been installed

Lastly if the database has not been initialized before run these commands

```
$ cd app/database
$ python init_db.py
$ cd ../..
```


### Building the frontend

The frontend is based on Angular2+ and styling using bootstrap 5.

## Running 

Start by building the frontend, this is done with the python script `build-frontend.py`

```$ python build-frontend.py```

To run the backend, execute the python scrip `EffectPlayerServer.py` in the root of the project.

```$ python EffectPlayerServer.py```


## Developing

### Developing the frontend

To develop on the frontend it can be nice to work against the backend, this can be done by starting the backed.

```$ python EffectPlayerServer.py```

Then navigate to `app/www/EffectPlayerClient` and run

```$ ng serve --proxy-config proxy.conf.json```

This will allow quick edits to the frontend without building and restarting the backend each time.
