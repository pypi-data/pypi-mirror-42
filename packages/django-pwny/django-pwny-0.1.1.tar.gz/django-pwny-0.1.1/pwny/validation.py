import hashlib

from django.core.exceptions import ValidationError

import requests


class HaveIBeenPwnedValidator:

    def validate(self, password, user=None):
        sha1 = hashlib.sha1()
        sha1.update(password.encode())
        digest = sha1.hexdigest().upper()
        prefix = digest[:5]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        r = requests.get(url, headers={"User-Agent": "django-pwny"})
        for suffix_count in r.text.splitlines():
            suffix, count = suffix_count.split(":")
            if digest ==f"{prefix}{suffix}":
                raise ValidationError( 
                    f"Your password has been pwned {count} times!"
                )

    def get_help_text(self):
        return (
            "Your password should not appear in a list of compromised "
            "passwords."
        )

