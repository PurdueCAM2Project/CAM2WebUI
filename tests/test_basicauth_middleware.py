"""Tests for basic authentication middleware.

This test module tests that a client providing incorrect credentials is returned
a 401 Unauthorized error while a client providing correct credentials is
directed to the intended page.

Run this test with pytest.

"""
import os
import base64


def test_basicauth(client):
    """Tests staging server basic authentication."""

    # return 401 with no credentials
    client.defaults['HTTP_AUTHORIZATION'] = format_credentials('username', 'password')
    response = client.get('', follow=True)
    assert response.status_code == 401

    client.defaults['HTTP_AUTHORIZATION'] = format_credentials(
        os.environ['BASICAUTH_USERNAME'], os.environ['BASICAUTH_PASSWORD'])
    response = client.get('', follow=True)
    assert response.status_code == 404

def format_credentials(username, password):
    """Helper function for formatting credentials.

    Username and password must be encoded as bytes before sending in a GET
    request. This function produces the correct value of the Authentication
    header given a username and password.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        A string suitable as the value of the Authentication header.

    """
    creds = '{}:{}'.format(username, password)
    creds_enc = base64.b64encode(creds.encode('utf-8')).decode('utf-8')
    return 'basic {}'.format(creds_enc)
