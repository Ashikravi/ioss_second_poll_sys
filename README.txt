REQUIREMENTS:  
- Python 3.8 or higher                                      
- Internet connection (for Bootstrap/Chart.js CDN)

SETUP INSTRUCTIONS:
1. EXTRACT PROJECT FILES
   - Unzip the project folder
   - Navigate to the project directory where manage.py is located

2. CREATE VIRTUAL ENVIRONMENT
   -python -m venv myenv
   


3. ACTIVATE VIRTUAL ENVIRONMENT
   Mac/Linux: source myenv/bin/activate
   Windows:   myenv\Scripts\activate

4. INSTALL DJANGO
   pip install django or (install all dependencies  " -pip install -r requirements.txt ")

5. SETUP DATABASE. 
   python manage.py makemigrations
   python manage.py migrate

6. CREATE ADMIN USER
   python manage.py createsuperuser
   (Enter username, email, and password)

7. START SERVER
   python manage.py runserver

8. OPEN BROWSER
   Go to: http://127.0.0.1:8000/





#VS code







