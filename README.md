Greeting: Hello, this is Solar Monitoring Application!
Author: Dmytro Buzoveria

Instruction:
1. Download and Install Python, use the latest version from https://www.python.org/downloads/.
2. Download and Install Postgres, use the latest version from https://www.postgresql.org/download/ (password use 123321).
3. Create database in PostgreSQL with name solar_project.
4. Once you are at the root of the project, run the following commands, one by one:
   - python3 -m venv venv (if doesn't work use python -m venv venv)
   - source venv/bin/activate (for Windows use .\venv\bin\activate)
   - pip install -r requirements.txt
   - uvicorn app.main:app --reload
5. Open in browser http://127.0.0.1:8000 for visit your site
6. If you have done everything correctly, and you see the forms for filling in the data, then congratulations, 
the program is working correctly
7. If you have some problems with this project please text me:
    @ArtArtas - Telegram
    shkolatlen@gmail.com - Gmail