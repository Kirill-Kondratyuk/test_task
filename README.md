
# INSTALLATION
## DOCKER
1. git clone https://github.com/Kirill-Kondratyuk/test_task
2. cd test_task
3. docker build . -t image_name
4. docker run image_name

## MANUAL RUN
1. git clone https://github.com/Kirill-Kondratyuk/test_task
2. cd test_task
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python models.py // Initialize db
7. python main.py
