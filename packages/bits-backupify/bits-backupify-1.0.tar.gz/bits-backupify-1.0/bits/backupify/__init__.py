"""Backupify class file."""

import json
import requests
import urllib
import urllib2


class Backupify(object):
    """Backupify Class."""

    def __init__(
        self,
        client_id,
        client_secret,
        base_url='https://api.backupify.com/gapps/v1/domains/',
        domain='broadinstitute.org',
        verbose=False
    ):
        """Initialize a class instance."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = '%s/%s' % (base_url, domain)
        self.verbose = verbose

        # headers
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }

        # authentication information
        self.access_token = None
        self.expires_in = None
        self.token_type = None

        # generate access token
        self.generate_access_token()

    def generate_access_token(self):
        """Generate access token."""
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'write',
        }
        url = 'https://api.backupify.com/oauth/token'
        response = requests.post(url, json=body).json()

        # save authentication information
        self.access_token = response.get('access_token')
        self.expires_in = response.get('expires_in')
        self.token_type = response.get('token_type')

        # update headers
        self.headers['Authorization'] = self.access_token

    def get_list_items(self, url, params, collection):
        """Get a URL."""
        # get first page of users
        response = requests.get(url, headers=self.headers, params=params).json()

        # get data from response
        next_page = response.get('next_page')
        total_entries = response.get('total_entries', 0)
        users = response.get(collection, [])

        # display info about response
        if self.verbose:
            print('Retrieved page %s with %s/%s results.' % (
                params['page'],
                len(users),
                total_entries,
            ))

        count = 1
        while next_page:
            response = requests.get(next_page, headers=self.headers).json()
            next_page = response.get('next_page')
            users.extend(response.get(collection, []))
            count += 1
            if self.verbose:
                print('Retrieved page %s with %s/%s results' % (
                    count,
                    len(users),
                    total_entries
                ))

        return users

    #
    # Users
    #
    def add_user(self, email):
        """Add a user to Backpify."""
        # POST https://api.backupify.com/gapps/v1/domains/{DomainName}/users -d 'user[email]={UserEmail}'
        url = '%s/users' % (self.base_url)
        data = {
            'user[email]': email,
        }
        return requests.post(url, json=data, headers=self.headers).json()

    def delete_user(self, email):
        """Delete a user from Backupify."""
        # DELETE https://api.backupify.com/gapps/v1/domains/{DomainName}/users/{UserEmail}
        url = '%s/users/%s' % (self.base_url, email)
        return requests.delete(url, headers=self.headers).json()

    def get_user(self, email):
        """Return a user from Backupify."""
        # GET https://api.backupify.com/gapps/v1/domains/{DomainName}/users/{UserEmail}
        url = '%s/users/%s' % (self.base_url, email)
        return requests.get(url, headers=self.headers).json()

    def get_users(self, status='all'):
        """List users in Backupify."""
        # GET https://api.backupify.com/gapps/v1/domains/{DomainName}/users
        url = '%s/users' % (self.base_url)
        params = {
            'page': 1,
            'per_page': 100,
            'status': status,
        }
        return self.get_list_items(url, params, 'users')

    #
    # Exports
    #
    def get_exports(self):
        """List exports."""
        # GET https://api.backupify.com/gapps/v1/domains/{DomainName}/services/{ServiceID}/exports
        # paginated

    #
    # Services
    #
    def get_service(self, service):
        """Get a service."""
        # GET https://api.backupify.com/gapps/v1/domains/{DomainName}/services/{ServiceID}
