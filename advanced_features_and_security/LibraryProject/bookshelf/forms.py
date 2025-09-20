# bookshelf/forms.py

from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Search books..."}),
        strip=True,
        help_text="Search by title or author"
    )

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        # Basic sanitization: trim and optionally remove suspicious characters
        q = q.strip()
        # More validation logic could be added here (length checks, regex)
        return q
