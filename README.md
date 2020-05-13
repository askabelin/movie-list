#### Install

python 3.7+ is required 

    pip install -r requirements.txt
    
### Test
    
    pytest
    
#### Run with real Redis

    FLASK_APP=movielist/server.py flask run -p 8000

#### Run with in-memory Redis

    USE_IN_MEMORY_REDIS=1 FLASK_APP=movielist/server.py flask run -p 8000
