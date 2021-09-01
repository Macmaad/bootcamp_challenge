# Go Bootcamp Challenge

## Explanation:

This app runs in `Python 3.7.3`, and uses `flask==2.0.1`. It has two endpoints, the first one is a really simple
one, it just returns "Hello world", and the second one works as a pokedex. If you like Pokemon, the pokedex is from 
Kanto region.

## Run the app:

To run the app you need to install everything inside the ./app/requirements.txt. 

```shell
pip install -r app/requierements.txt
```

Then you just need to do 

```shell
python app/app.py
```

This way you will see that the flask is running, and it is pointing to your local host in port 5000 
`http://127.0.0.1:5000/`. 

To retrieve the hello world you just need to call `http://127.0.0.1:5000/` and for the pokedex you should call
`http://127.0.0.1:5000/pokdex/<pokemon_id>`, you can select a pokemon id between 1 and 150. 

## Testing

Tu run your test you will need to have `pytest==6.2.5` installed and run:

```shell
python -m pytest test/
```

