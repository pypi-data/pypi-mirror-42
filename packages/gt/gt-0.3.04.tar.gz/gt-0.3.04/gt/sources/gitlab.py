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
        self._user = None
        
    def user(self):
        if not self._user:
            r = re.search('username="([^"]*)', self.http.get('https://gitlab.com').text)
            if not r:
                raise Exception("Invalid private token supplied: " + token)
            self._user = r.group(1)
        
        return self._user
        

    def list(self):
        page = 1
        res = []

        while True:
            resp = self.http.get('https://gitlab.com/api/v4/projects?owned=true&per_page=100&page=' + str(page))
            page = resp.headers['X-Next-Page']
            res += [  (r['name'], r['visibility'] == 'private') for r in resp.json() ]
            if not page: break

        return res


    def delete(self, name):
        project_url = 'https://gitlab.com/' + self.user() + "/" + name
        r = self.http.get(project_url)
        if(r.status_code != 200):
            raise Exception("Project \"{0}\" does not seem to exist.".format(name))
        
        root = bs4.BeautifulSoup(r.text, 'html.parser')
        token = root.find(attrs={'name': 'csrf-token'})['content']

        r = self.http.post(project_url, {
            '_method': 'delete',
            'authenticity_token': token
        })
        if(r.status_code != 200):
            raise Exception("Failed to delete project, request output: \n\n" + r.text)


    def location(self, name):
        return "ssh://git@gitlab.com:/" + self.user() + "/" + name
    
    def create(self, name, description='', is_private=True):
        r = self.http.get('https://gitlab.com/projects/new')

        root = bs4.BeautifulSoup(r.text, 'html.parser')
        auth_token = root.find('meta', attrs={'name': 'csrf-token'})['content']
        users = root.find('select',
                          attrs={'name':
                                 'project[namespace_id]'})\
                    .find('optgroup',
                          attrs={'label': 'Users'})

        assert len(list(users.children)) == 1
        namespace_id = next(users.children)['value']

        params = {
            'utf8': '✓',
            'authenticity_token': auth_token,
            'project[namespace_id]': namespace_id,
            'project[path]': name,
            'project[description]': description,
            'project[visibility_level]': 0 if is_private else 20
        }
    
        r = self.http.post('https://gitlab.com/projects', params)
    
        if 'was successfully created.' not in r.text:
            raise Exception("Failed to create repo: {0}. Make sure it does not already exist."\
                            .format(name))
