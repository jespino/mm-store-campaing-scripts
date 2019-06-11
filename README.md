# Mattermost Store Campaign Scripts

## Fork it

If you want to create your own campaign, you should fork this repo and modify
the `create_jira_ticket.py` script to add your own variables (for your template).

## Examples of usage

For create a new jira ticket for the campaing you can execute:

```sh
python create_jira_ticket.py --username jesus@mattermost.com --token xxxxxxxxxxxxxxxxxxxxxxxx --store Channel --method Delete
```

It will create a jira ticket based on the template, and the data that you
provided using your username and token to access Jira.

After all the jira tickets are created, you can modify them with a batch update
and add the "Help Wanted" Fix version, then in a short period of time (some
minutes) it will be created in github automatically.

After the creation you can tag them using the `github_tags.py` script, executing for example:

```sh
python github_tags.py --token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -r mattermost/mattermost-server -l "Tech/Go" -l "Up For Grabs" -l "Difficulty/1:Easy" -l "Area/Technical Debt" -l "Help Wanted" 1234051
```

in this case the final number is the github issue number (you can pass multiple
issue numbers if you want).
