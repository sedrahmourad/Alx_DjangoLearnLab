Security measures applied (summary)

\- DEBUG=False in production and ALLOWED\_HOSTS configured.

\- SESSION\_COOKIE\_SECURE and CSRF\_COOKIE\_SECURE set to True (cookies over HTTPS only).

\- SECURE\_BROWSER\_XSS\_FILTER, SECURE\_CONTENT\_TYPE\_NOSNIFF, X\_FRAME\_OPTIONS set.

\- CSP applied via django-csp middleware OR header set in middleware/views.

\- Forms validated using Django Form classes; search view uses ORM queries (no string formatting).

\- Avoided raw SQL; if using raw() use parameterized args.

\- Templates rely on Django autoescape; do not use |safe on untrusted content.

Testing steps: see project README or run manual tests for CSRF/XSS/SQLi and header checks.



