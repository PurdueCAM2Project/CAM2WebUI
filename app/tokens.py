from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Generates a token used to activate an account through a link

    Uses the Django implementation of six to generate a hash specific to the user
    to be used when the user is validated via an account activation link

    """
    def _make_hash_value(self, user, timestamp):
        """Generates a hash value for a user's account activation link

        Uses django.utils.six to create a hash based on the user and the time
        of submisson.

        Args:
            user: the user who requested an account
            timestamp: the time at which the user submitted the registration form

        Returns:
            a hashed value based on the user who submitted the form and the time
            of sumbission.
        
        """
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.registeruser.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
