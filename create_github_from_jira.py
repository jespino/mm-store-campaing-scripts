import click
import requests
import pprint
from requests.auth import HTTPBasicAuth
from github import Github

import sys
reload(sys)
sys.setdefaultencoding('utf8')

footer = '''
----

If you're interested please comment here and come [join our "Contributors" community channel](https://community.mattermost.com/core/channels/tickets) on our daily build server, where you can discuss questions with community members and the Mattermost core team. For technical advice or questions, please [join our "Developers" community channel](https://community.mattermost.com/core/channels/developers).

New contributors please see our [Developer's Guide](https://developers.mattermost.com/contribute/getting-started/).

JIRA: https://mattermost.atlassian.net/browse/MM-{{TICKET}}
'''

@click.command()
@click.option('--jira-token', '-j', prompt='Your Jira access token', help='The token used to authenticate the user against Jira.')
@click.option('--jira-username', '-u', prompt='Your Jira username', help='Username of the user to get the ticket information.')
@click.option('--github-token', '-g', prompt='Your Github access token', help='The token used to authenticate the user against Github.')
@click.option('--repo', '-r', prompt='Repository', help='The repository which contains the issues. E.g. mattermost/mattermost-server')
@click.option('--labels', '-l', prompt='Labels', help='The labels to set to the issues', multiple=True)
@click.option('--dry-run/--no-dry-run', help='Skip actually creating any tickets', default=False)
@click.option('--debug/--no-debug', help='Dump debugging information.', default=False)
@click.argument('issue-numbers', nargs=-1)
def cli(jira_token, jira_username, github_token, repo, labels, dry_run, debug, issue_numbers):
    if len(issue_numbers) < 1:
        print("You need to pass at least one issue number")
        return

    g = Github(github_token)
    r = g.get_repo(repo)
    final_labels = []
    for label in r.get_labels():
        if label.name in labels:
            final_labels.append(label)

    for issue_number in issue_numbers:
        resp = requests.get(
            "https://mattermost.atlassian.net/rest/api/3/issue/MM-"+issue_number,
            auth=HTTPBasicAuth(jira_username, jira_token)
        )
        data = resp.json()

        if debug:
            pprint.pprint(data)

        renderedContent = []
        lastLanguage = ''
        for content in data['fields']['description']['content']:
            # Keep track of the last language seen to annotate the next code block encountered.
            if 'attrs' in content:
                if 'language' in content['attrs']:
                    lastLanguage = content['attrs']['language']

            if content['type'] == 'codeBlock':
                renderedContent.append("```" + lastLanguage + "\n" + content['content'][0]['text'] + "\n```")
                lastLanguage = ''

            elif content['type'] == 'paragraph':
                elements = []
                for element in content['content']:
                    if element['type'] == 'text':
                        text = element['text']

                        # Resolve inline code or links
                        if 'marks' in element:
                            if 'type' in element['marks'][0]:
                                if element['marks'][0]['type'] == 'code':
                                    text = '`' + text + '`'
                                if element['marks'][0]['type'] == 'link':
                                    text = '[' + text + '](' + element['marks'][0]['attrs']['href'] + ')'

                        elements.append(text)

                renderedContent.append("".join(elements))

        title = data['fields']['summary']
        description = "\n\n".join(renderedContent) + "\n" + footer.replace("{{TICKET}}", issue_number)

        if dry_run:
            print '''We haven't created the github ticket because --dry-run flag was detected. Ticket information:

{}
{}

{}
'''.format(title, "=" * len(title), description)
            return

        try:
            new_issue = r.create_issue(
                title=title,
                body=description,
                labels=final_labels,
            )
        except Exception as e:
            print("Unable to create issue for jira issue {}. error: {}".format(issue_number, e))
            return

        print("Created ticket: {}".format(new_issue.html_url))

        try:
            resp = requests.put(
                "https://mattermost.atlassian.net/rest/api/3/issue/MM-"+issue_number,
                json={
                    "fields": {
                        "customfield_11106": new_issue.html_url,
                        "fixVersions": [{"name": "Help Wanted"}]
                    },
                },
                auth=HTTPBasicAuth(jira_username, jira_token)
            )
        except Exception as e:
            print("Unable to update jira issue {}. error: {}".format(issue_number, e))
            return

if __name__ == "__main__":
    cli()
