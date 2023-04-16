from bottle import run
import controller  

if __name__ == "__main__":
    ssl_cert_file = 'C:\\Users\\Admin\\certs\\hellfish.test.crt'
    ssl_key_file = 'C:\\Users\\Admin\\certs\\hellfish.test.key'

    run(server='wsgiref', host='localhost', port=443, debug=True, ssl_context=(ssl_cert_file, ssl_key_file))


    