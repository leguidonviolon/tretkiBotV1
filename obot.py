import praw

app_id = "ZA318USVt7IwWg"
app_secret = "5kqibzqVqLLJ1qkOKhJgVZXXZbE"
app_uri = "https://127.0.0.1:65010/authorize_callback"
app_ua = "bulo_bot made by /u/oniixon.  Manages /r/bulo, adds and kicks members, etc.  V2.0"
app_scopes = "account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread"
app_account_code = "Moso0mptcQBKVyBo1qNwPzaLECA"
app_refresh = "8FH8UAU-MLEZM2QKcV0T_XFNpn0"

def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r
