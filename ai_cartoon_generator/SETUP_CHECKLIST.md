# ✅ Setup Checklist - AI Cartoon Generator

Use this checklist to ensure your authentication system is properly configured and working.

---

## 📋 Pre-Installation

- [ ] Python 3.10+ installed
- [ ] PostgreSQL 15+ installed
- [ ] Text editor/IDE installed (VS Code recommended)
- [ ] Git installed (optional but recommended)
- [ ] Modern web browser (Chrome, Firefox, Edge)

---

## 🔧 Installation Steps

### Step 1: Project Setup
- [ ] Project folder created/downloaded
- [ ] Opened terminal/command prompt in project directory
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] Dependencies installed (`pip install -r requirements.txt`)

### Step 2: Configuration
- [ ] `.env` file created from `.env.example`
- [ ] SECRET_KEY generated and added to `.env`
- [ ] DEBUG set to `True` in `.env`
- [ ] ALLOWED_HOSTS configured in `.env`

### Step 3: Database Setup
- [ ] PostgreSQL service is running
- [ ] Database `ai_cartoon_db` created
- [ ] Database connection details added to `.env`:
  - [ ] DB_NAME
  - [ ] DB_USER
  - [ ] DB_PASSWORD
  - [ ] DB_HOST
  - [ ] DB_PORT
- [ ] Database connection tested (try connecting with psql)

### Step 4: Django Setup
- [ ] Migrations created (`python manage.py makemigrations`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] No migration errors shown
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Superuser credentials saved securely

---

## 🧪 Testing Basic Functionality

### Server Test
- [ ] Development server starts without errors
- [ ] Server accessible at http://localhost:8000/
- [ ] No 500 errors in terminal

### Admin Panel Test
- [ ] Admin panel accessible at http://localhost:8000/admin/
- [ ] Can login with superuser credentials
- [ ] Can see "Users" in admin panel
- [ ] Can view user list
- [ ] Can create a test user in admin

### Registration Test
- [ ] Registration page loads http://localhost:8000/accounts/register/
- [ ] Page displays correctly (no broken CSS/images)
- [ ] All form fields visible:
  - [ ] Full Name
  - [ ] Username
  - [ ] Email
  - [ ] Password
  - [ ] Confirm Password
  - [ ] Terms checkbox
- [ ] Can submit form with valid data
- [ ] Success message appears after registration
- [ ] Redirected to login page
- [ ] New user appears in database/admin panel

### Login Test
- [ ] Login page loads http://localhost:8000/accounts/login/
- [ ] Page displays correctly
- [ ] Can login with username
- [ ] Can login with email
- [ ] Remember me checkbox works
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard

### Dashboard Test
- [ ] Dashboard loads http://localhost:8000/dashboard/
- [ ] Welcome message shows user's name
- [ ] Profile information displayed
- [ ] Logout button visible
- [ ] Can access dashboard only when logged in
- [ ] Redirects to login when not authenticated

### Logout Test
- [ ] Logout button works
- [ ] Success message appears
- [ ] Redirected to login page
- [ ] Cannot access dashboard after logout

---

## 🎨 UI/Design Verification

### Visual Checks
- [ ] Sky-blue theme colors visible
- [ ] Glassmorphism effects working
- [ ] Background gradients showing
- [ ] Cards have rounded corners
- [ ] Hover animations working
- [ ] Bootstrap Icons displaying
- [ ] No broken images

### Form Features
- [ ] Password visibility toggle working (eye icon)
- [ ] Form fields have proper styling
- [ ] Validation errors show in red
- [ ] Success messages show in green
- [ ] Auto-dismiss alerts working (5 seconds)

### Responsive Design
- [ ] Desktop view (1920px+) looks good
- [ ] Tablet view (768px) looks good
- [ ] Mobile view (375px) looks good
- [ ] Navigation menu works on mobile
- [ ] Forms are readable on all screen sizes

---

## 🔒 Security Verification

### CSRF Protection
- [ ] Forms with method="POST" have {% csrf_token %}
- [ ] Form submission without CSRF token fails

### Password Security
- [ ] Weak passwords rejected (less than 8 chars)
- [ ] Passwords without numbers rejected
- [ ] Passwords without special chars rejected
- [ ] Password confirmation mismatch rejected
- [ ] Passwords stored as hashes (not plain text)

### Validation
- [ ] Duplicate username rejected
- [ ] Duplicate email rejected
- [ ] Invalid email format rejected
- [ ] Client-side validation working (JavaScript)
- [ ] Server-side validation working (Django)

### Route Protection
- [ ] Cannot access /dashboard/ when logged out
- [ ] Redirects to login with ?next parameter
- [ ] After login, redirects to intended page

---

## 🔐 Google OAuth Setup (Optional)

If setting up Google OAuth:

### Google Cloud Console
- [ ] Google Cloud project created
- [ ] Google+ API enabled
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created (Client ID & Secret)
- [ ] Authorized JavaScript origins added:
  - [ ] http://localhost:8000
  - [ ] http://127.0.0.1:8000
- [ ] Authorized redirect URIs added:
  - [ ] http://localhost:8000/auth/google/login/callback/
  - [ ] http://127.0.0.1:8000/auth/google/login/callback/
- [ ] Test user email added (for development)

### Django Configuration
- [ ] GOOGLE_CLIENT_ID added to `.env`
- [ ] GOOGLE_CLIENT_SECRET added to `.env`
- [ ] Site configured in Django admin (localhost:8000)
- [ ] Social application created in Django admin
- [ ] Google provider configured with credentials

### Testing Google OAuth
- [ ] "Continue with Google" button visible
- [ ] Clicking button redirects to Google
- [ ] Can select Google account
- [ ] Redirected back to dashboard
- [ ] User created automatically in database
- [ ] Profile picture from Google displayed
- [ ] Full name from Google saved

---

## 📝 Code Quality Checks

### Python Code
- [ ] No syntax errors
- [ ] No import errors
- [ ] No undefined variables
- [ ] Proper indentation
- [ ] Comments present
- [ ] Docstrings for functions

### Templates
- [ ] Valid HTML (no unclosed tags)
- [ ] {% load static %} present where needed
- [ ] {% csrf_token %} in POST forms
- [ ] Template inheritance working
- [ ] All variables defined

### Static Files
- [ ] CSS file loading
- [ ] JavaScript file loading
- [ ] No console errors in browser
- [ ] Images loading (if any)

---

## 🧪 Advanced Testing

### Database Operations
- [ ] Can create users
- [ ] Can update users
- [ ] Can delete users
- [ ] Timestamps working (created_at, updated_at)
- [ ] Default values working

### Session Management
- [ ] Session created on login
- [ ] Session persists across page loads
- [ ] "Remember me" extends session
- [ ] Session cleared on logout

### Messages Framework
- [ ] Success messages show (green)
- [ ] Error messages show (red)
- [ ] Messages auto-dismiss
- [ ] Multiple messages can show

### Error Handling
- [ ] 404 page for invalid URLs (Django default)
- [ ] Error messages user-friendly
- [ ] No sensitive information in errors
- [ ] Errors logged properly

---

## 📦 Deployment Readiness (Optional)

For production deployment:

### Configuration
- [ ] DEBUG=False in production .env
- [ ] New SECRET_KEY generated for production
- [ ] ALLOWED_HOSTS set to domain name
- [ ] Database credentials for production added
- [ ] Google OAuth URIs updated for production

### Static Files
- [ ] `collectstatic` runs without errors
- [ ] Static files served correctly
- [ ] CSS/JS working in production

### Security
- [ ] HTTPS enabled
- [ ] SSL certificate valid
- [ ] Security headers configured
- [ ] HSTS enabled
- [ ] Secure cookies enabled

### Performance
- [ ] Database indexed
- [ ] Static files cached
- [ ] Database connection pooling
- [ ] Gunicorn configured

---

## 🎯 Success Criteria

Your setup is complete when:

✅ **All core features work**
- Registration ✓
- Login (username & email) ✓
- Logout ✓
- Dashboard access ✓
- Protected routes ✓

✅ **Security is solid**
- CSRF protection ✓
- Password validation ✓
- Unique constraints ✓
- Route protection ✓

✅ **UI looks professional**
- Sky-blue theme ✓
- Responsive design ✓
- Smooth animations ✓
- No broken elements ✓

✅ **Google OAuth works** (if configured)
- Google login ✓
- User auto-creation ✓
- Profile picture ✓

---

## 🐛 Common Issues Quick Fix

### Issue: Cannot activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: Database connection error
```bash
# Check PostgreSQL is running
# Windows: Services → PostgreSQL → Start
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Migrations error
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Port 8000 in use
```bash
python manage.py runserver 8080
```

---

## 📞 Getting Help

If issues persist:

1. Check [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md) for detailed explanations
2. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
3. Read error messages carefully
4. Check Django logs in terminal
5. Verify all steps above are completed
6. Search Stack Overflow
7. Check Django documentation

---

## 🎉 Congratulations!

If you've checked all the boxes above, your AI Cartoon Generator authentication system is:

✅ Fully functional
✅ Secure
✅ Production-ready
✅ Beginner-friendly
✅ Ready for AI features

**You're ready to start adding the AI cartoon transformation features!** 🚀

---

**Print this checklist and check off items as you complete them.**

Last Updated: 2026-02-17
Version: 1.0.0
