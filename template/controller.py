'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

import json
from bottle import route, get, post, error, request, static_file
from cryptography.fernet import Fernet
import base64
import model
import sql
#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# # Allow CSS
# @route('/css/<css:path>')
# def serve_css(css):
#     '''
#         serve_css

#         Serves css from static/css/

#         :: css :: A path to the requested css

#         Returns a static file object containing the requested css
#     '''
#     return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# # Allow javascript
# @route('/js/<js:path>')
# def serve_js(js):
#     '''
#         serve_js

#         Serves js from static/js/

#         :: js :: A path to the requested javascript

#         Returns a static file object containing the requested javascript
#     '''
#     return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------


# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the friend list page for Andy
@get('/Andy')
def get_Andy_controller():
    '''
        get_Andy
        Serves the friend list page for Andy
    '''
    return model.friend()





# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.login_check(username, password)

# Generate a 32-byte key that is url-safe
key = Fernet.generate_key()
key = base64.urlsafe_b64encode(key[:32])

# Create a Fernet object with the key
fernet = Fernet(key)


# Function to handle sending messages
@post('/send_message')
def send_message():
    # Get the message from the request
    message = request.forms.get('message')

    # Encrypt the message with Fernet
    encrypted_message = fernet.encrypt(message.encode())

    # Send the encrypted message to Andy
    model.send_message('Andy', encrypted_message)

    # Return a success message
    return json.dumps({'status': 'success'})

# Function to handle receiving messages
@get('/get_messages')
def get_messages():
    # Get the messages from the model
    messages = model.get_messages('Andy')

    # Decrypt the messages with Fernet
    decrypted_messages = []
    for message in messages:
        decrypted_message = fernet.decrypt(message.encode()).decode()
        decrypted_messages.append(decrypted_message)

    # Return the decrypted messages as JSON
    return json.dumps({'messages': decrypted_messages})


# Function to handle getting the conversation
@get('/get_conversation')
def get_conversation():
    '''
        get_conversation
        Returns the conversation between Andy and the current user
    '''

    # Get the conversation between the two users
    conversation = sql.get_conversation('Andy', 'current_user')

    # Decrypt the messages with Fernet
    decrypted_messages = []
    for message in conversation:
        decrypted_message = fernet.decrypt(message.encode()).decode()
        decrypted_messages.append(decrypted_message)

    # Return the decrypted messages as JSON
    return json.dumps({'messages': decrypted_messages})



#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
