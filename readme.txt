How to use and create installer

1. Create a virtual environment
    python -m venv venv
2. Activate virtual environment
    .\venv\Scripts\Activate
3. When virtual environment is activated install neccessary packages for astro
    pip install -r requirements.txt
4. When all requirements are installed you can test the app inside the virtual environment 
    python astro.py
5. When all are ok during testing you can Create installer from script 
    pyinstaller --noconsole --onefile --icon=startup.ico astro.py
    Note: You may need to add the astro.ui & startup.png to the dist folder after creating an executable file