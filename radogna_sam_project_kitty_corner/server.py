from flask_app import app
from flask_app.controllers import home, kitties, users
from flask_app.models import kitty, user










if __name__=="__main__":   
    app.run(debug=True, host="localhost", port=3000) 
