# Python Checkit

### Installazione

Per installare la libreria e' sufficiente digitare:

        pip install python-checkit

### Utilizzo

Inizializzare l'oggetto Checkit utilizzando una chiave API valida:

```python

checkit = Checkit(api_key="<CHECKIT_API_KEY>")

```

Per controllare una carta di credito:

```python

result = checkit.creditcard.check("4242424242424242")

```

