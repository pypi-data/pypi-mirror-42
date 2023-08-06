import requests
import bs4
import re
from gt.sources.base import GitSource

class Gitlab(GitSource):
    """
    Class for manipulating private projects hosted by gitlab (the service).
    Scraping is used in place of the API which is painfully slow
    (see https://gitlab.com/gitlab-com/support-forum/issues/576 and
    https://gitlab.com/gitlab-com/gl-infra/infrastructure/issues/59). The 
    constructor consumes an API access token which can be generated
    here: https://gitlab.com/profile/personal_access_tokens.
    """
    
    def __init__(self, name, api_token):
        self.name = name
        self.http = requests.Session()
        self.http.headers.update({'PRIVATE-TOKEN': api_token})
        
    def list(self):
        page = 1
        res = []
        self._repo_cache = {}

        while True:
            resp = self.http.get('https://gitlab.com/api/v4/projects?owned=true&per_page=100&page=' + str(page))
            page = resp.headers['X-Next-Page']
            res += [  (r['name'], r['visibility'] == 'private') for r in resp.json() ]
            self._repo_cache.update({ r['name']: r for r in resp.json() })
            if not page: break

        return res


    def delete(self, name):
        if not hasattr(self, '_repo_cache'):
            self.list()

        _id = self._repo_cache[name]['id']
        r = self.http.delete('https://gitlab.com/api/v4/projects/' + str(_id))
        if r.status_code != 202:
            raise Exception()

    def location(self, name):
        if not hasattr(self, '_repo_cache'):
            self.list()

        return 'ssh://' + self._repo_cache[name]['ssh_url_to_repo']
    
    def create(self, name, description='', is_private=True):
        r = self.http.post('https://gitlab.com/api/v4/projects', {'path': name, 'description': description})
        if r.status_code != 201:
            raise Exception('Gitlab creation failed (project already exists?).')
