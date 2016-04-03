from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
import gdata.sites.client
import gdata.sites.data

# How to use the OAuth 2.0 client is described here:
# https://developers.google.com/api-client-library/python/guide/aaa_oauth

SCOPE = 'https://sites.google.com/feeds/'

# client_secrets.json is downloaded from the API console:
# https://code.google.com/apis/console/#project:<PROJECT_ID>:access
# where <PROJECT_ID> is the ID of your project

flow = flow_from_clientsecrets('client_secrets.json',
                               scope=SCOPE,
                               redirect_uri='http://localhost')

storage = Storage('plus.dat')
credentials = storage.get()

if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

# Munge the data in the credentials into a gdata OAuth2Token
# This is based on information in this blog post:
# https://groups.google.com/forum/m/#!msg/google-apps-developer-blog/1pGRCivuSUI/3EAIioKp0-wJ

auth2token = gdata.gauth.OAuth2Token(client_id=credentials.client_id,
  client_secret=credentials.client_secret,
  scope=SCOPE,
  access_token=credentials.access_token,
  refresh_token=credentials.refresh_token,
  user_agent='sites-test/1.0')

# Create a gdata client

client = gdata.sites.client.SitesClient(source='sites-test',
                                        site='YOUR_SITE',
                                        domain='YOUR_DOMAIN',
                                        auth_token=auth2token)

# Authorize it

auth2token.authorize(client)

# Call an API e.g. to get the site content feed

feed = client.GetContentFeed()

for entry in feed.entry:
    print '%s [%s]' % (entry.title.text, entry.Kind())

# See:
# https://developers.google.com/google-apps/sites/docs/1.0/developers_guide_python
# for more details of the Sites API