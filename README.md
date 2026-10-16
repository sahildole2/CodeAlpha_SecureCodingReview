# CodeAlpha Task 3 - Secure Coding Review

**Language / App:** Python (Flask) - `vulnerable_app.py`
**Method:** Manual code inspection + Bandit static analysis (`pip install bandit` then `bandit vulnerable_app.py`)
**Author:** Sahil Dole

## Findings

| # | Vulnerability | Where | Severity | Why it is dangerous |
|---|---|---|---|---|
| 1 | SQL Injection (CWE-89) | `/login` | High | Attacker types `' OR '1'='1' --` as username and logs in without a password. |
| 2 | OS Command Injection (CWE-78) | `/ping` | Critical | `host=8.8.8.8; cat /etc/passwd` runs extra commands on the server. |
| 3 | Cross-Site Scripting / XSS (CWE-79) | `/hello` | Medium | `?name=<script>...</script>` runs JavaScript in the victim's browser. |
| 4 | Hardcoded secret key (CWE-798) | `secret_key` | Medium | Anyone with the code can forge session cookies. |
| 5 | Plaintext passwords (CWE-256) | `/login` query | High | If the DB leaks, all passwords are exposed. |
| 6 | Debug mode + bind 0.0.0.0 (CWE-489) | `app.run` | High | Flask debugger allows remote code execution and exposes the app to the whole network. |

## Fixes

### 1. SQL Injection: use parameterized queries
```python
user = db().execute(
    "SELECT password_hash FROM users WHERE username=?", (username,)
).fetchone()
```

### 2. Command Injection: no shell, validate input
```python
import subprocess, ipaddress
try:
    ipaddress.ip_address(host)          # sirf valid IP allow
except ValueError:
    return "Invalid host", 400
out = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
return out.stdout
```

### 3. XSS: escape output
```python
from markupsafe import escape
return f"<h1>Hello {escape(name)}</h1>"
```

### 4. Secret key: environment variable
```python
app.secret_key = os.environ["SECRET_KEY"]
```

### 5. Passwords: hash them
```python
from werkzeug.security import generate_password_hash, check_password_hash
# signup: generate_password_hash(password)
# login : check_password_hash(stored_hash, password)
```

### 6. Debug off in production
```python
app.run(debug=False, host="127.0.0.1")   # production me gunicorn + reverse proxy
```

## General best practices
- Never trust user input: validate, sanitize, escape.
- Least privilege for DB users and app processes.
- Keep dependencies updated (`pip list --outdated`, `pip-audit`).
- Use HTTPS everywhere.
- Run static analysis (Bandit) in every project.
- Don't commit secrets to GitHub (use `.env` + `.gitignore`).

## Conclusion
The sample app had 6 vulnerabilities, three of them (SQLi, command injection, XSS) are in the OWASP Top 10 categories. All can be fixed with small code changes shown above.
