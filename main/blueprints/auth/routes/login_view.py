from flask import Blueprint, render_template
from .. import auth_bp

@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')  


