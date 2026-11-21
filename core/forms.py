from django import forms

from .models import Message


class ContactForm(forms.ModelForm):
    # champ piège anti-spam : doit rester vide
    website = forms.CharField(required=False)

    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("spam")
        return ""
