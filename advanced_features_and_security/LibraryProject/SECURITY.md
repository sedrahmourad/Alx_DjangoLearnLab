Security measures applied (summary)

\- DEBUG=False in production and ALLOWED\_HOSTS configured.

\- SESSION\_COOKIE\_SECURE and CSRF\_COOKIE\_SECURE set to True (cookies over HTTPS only).

\- SECURE\_BROWSER\_XSS\_FILTER, SECURE\_CONTENT\_TYPE\_NOSNIFF, X\_FRAME\_OPTIONS set.

\- CSP applied via django-csp middleware OR header set in middleware/views.

\- Forms validated using Django Form classes; search view uses ORM queries (no string formatting).

\- Avoided raw SQL; if using raw() use parameterized args.

\- Templates rely on Django autoescape; do not use |safe on untrusted content.

Testing steps: see project README or run manual tests for CSRF/XSS/SQLi and header checks.



\# Django Security Hardening



\## HTTPS and Secure Redirects

\- All HTTP requests are redirected to HTTPS via `SECURE\_SSL\_REDIRECT=True`.

\- HSTS is enforced for 1 year (`SECURE\_HSTS\_SECONDS=31536000`) with subdomains included and preload enabled.

\- Session and CSRF cookies are restricted to HTTPS with `SESSION\_COOKIE\_SECURE=True` and `CSRF\_COOKIE\_SECURE=True`.



\## Secure Headers

\- X-Frame-Options set to DENY → prevents clickjacking.

\- SECURE\_CONTENT\_TYPE\_NOSNIFF=True → prevents MIME sniffing.

\- SECURE\_BROWSER\_XSS\_FILTER=True → enables browser XSS filter.



\## Deployment Notes

\- SSL/TLS certificates provisioned using Let's Encrypt.

\- Nginx is configured to redirect all HTTP to HTTPS and serve certificates.



\## Review

These settings enforce encrypted communication, secure cookies, and safe headers.

Potential improvements:

\- Add CSP (Content Security Policy) to further mitigate XSS.

\- Use nonces/hashes for inline scripts in templates.



