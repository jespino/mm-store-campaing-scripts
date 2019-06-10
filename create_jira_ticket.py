import requests
import click
from requests.auth import HTTPBasicAuth

@click.command()
@click.option('--username', prompt='Your username', help='Username of the user to publish the new user story.')
@click.option('--token', prompt='Your user token', help='The token used to authenticate the user.')
@click.option('--store', prompt='Store', help='Store')
@click.option('--method', prompt='Method', help='Method')
def cli(username, token, store, method):
    template = open("template.md").read()

    summary = "Migrate \"{}.{}\" to Sync by default".format(store, method)

    description = template.replace("{{store}}", store)
    description = description.replace("{{method}}", method)

    data = {
        "fields": {
            "project": {"key": "MM"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"},
            "customfield_11101": {"value": "Platform"},
        }
    }

    resp = requests.post(
        "https://mattermost.atlassian.net/rest/api/2/issue/",
        json=data,
        auth=HTTPBasicAuth(username, token)
    )
    print("https://mattermost.atlassian.net/browse/{}".format(resp.json()['key']))

if __name__ == "__main__":
    cli()
