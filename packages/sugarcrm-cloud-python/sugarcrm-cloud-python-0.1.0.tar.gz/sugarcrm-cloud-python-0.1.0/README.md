# sugarcrm-cloud-python
API wrapper for SugarCRM cloud written in Python

This support API v10+ and v11+

## Installing
```
pip install sugarcrm-cloud-python
```

## Usage
```
from sugarcrm.client import Client

client = Client('site_url', version='8.3') # sugarcrm cloud instance version not API version
```

Get user token
```
client.get_token('username', 'password')
```

Set access token to library
```
client.set_access_token('access_token')
```

Refresh user token
```
client.get_token('refresh_token')
```

Get account information
```
client.me()
```

Get leads
```
client.get_leads()
```

Get a lead
```
client.get_lead('lead_id')
```

Filter leads
```
client.filter_leads(filter_expr=[{'first_name': 'Dave'}])
```

Create a lead
```
client.create_lead({"first_name": "Dave", "last_name": "Smith", "assistant": "Mike Smith"})
```

Get contacts
```
client.get_contacts()
```

Get a contact
```
client.get_contact('contact_id')
```

Filter contacts
```
client.filter_contacts(filter_expr=[{'first_name': 'Dave'}])
```

Create a contact
```
client.create_contact({"first_name": "Dave", "last_name": "Smith", "assistant": "Mike Smith"})
```

Get module fields metadata
```
response = client.get_metadata('Leads')
fields = response['modules']['Leads']['fields']
```

## Requirements
- requests

## TODO
- All other modules

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.

#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/sugarcrm-cloud-python/issues).

#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/sugarcrm-cloud-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
