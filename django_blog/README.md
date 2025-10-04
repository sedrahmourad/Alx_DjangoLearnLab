Authentication System Documentation

1. Features Implemented

Registration: New users can register with username, email, and password.

Login/Logout: Users authenticate and end sessions securely.

Profile Management: Users can view and edit profile details (like email, bio, picture).

2. How It Works

Registration: Uses UserCreationForm extended with email. Data is validated, password is hashed.

Login: Uses Django’s built-in LoginView.

Logout: Uses Django’s built-in LogoutView.

Profile: Custom view with @login_required to restrict access.

3. Security Measures

CSRF protection in all forms ({% csrf_token %}).

Passwords stored with Django’s password hashing.

Profile and sensitive pages protected with @login_required.

4. Testing Instructions

Navigate to /register → Register a new user.

Navigate to /login → Login with your new credentials.

Navigate to /profile → Edit your profile and save changes.

Click /logout → Confirm you are logged out.