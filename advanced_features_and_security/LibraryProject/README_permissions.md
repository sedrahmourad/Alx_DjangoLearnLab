\# Permissions and Groups Setup



\## Custom Permissions

Defined in `Book` model (`relationship\_app/models.py`):

\- can\_view

\- can\_create

\- can\_edit

\- can\_delete



\## Groups

Created via Django Admin:

\- \*\*Viewers\*\*: can\_view

\- \*\*Editors\*\*: can\_view, can\_create, can\_edit

\- \*\*Admins\*\*: can\_view, can\_create, can\_edit, can\_delete



\## Views with Permission Checks

\- `book\_list` → requires can\_view

\- `create\_book` → requires can\_create

\- `edit\_book` → requires can\_edit

\- `delete\_book` → requires can\_delete



