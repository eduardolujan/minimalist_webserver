# minimalist_webserver by Mario Chavez


## Install packages

```
$ pip install -r requirements/base
```
## Rules
```
# Method not allowed 
http GET 'http://127.0.0.1:9292' 

# Not acceptable request 
http POST 'http://127.0.0.1:9292' Accept:"application/xml" 

# Bad request 
http POST 'http://127.0.0.1:9292' Accept:"application/json" Content-Type:"application/xml" name="michelada" email="hello@michelada.io" 
http POST 'http://127.0.0.1:9292' Accept:"application/json" Content-Type:"application/json" 

# Error, missing or empty name or email 
http POST 'http://127.0.0.1:9292' Accept:"application/json" Content-Type:"application/json" name="michelada" emails="hello@michelada.io" 

# Successful 
http POST 'http://127.0.0.1:9292' Accept:"application/json" Content-Type:"application/json" name="michelada" email="hello@michelada.io" 
http POST 'http://127.0.0.1:9292' Content-Type:"application/json" name="michelada" email="hello@michelada.io"

```

