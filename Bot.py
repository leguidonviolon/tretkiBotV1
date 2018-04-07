#!/usr/bin/env python

import praw, datetime, time, random, string, obot

today = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().year)


def log(m, show=True):
    logs = open("FILE PATH"+ today +".txt", "a")  #EDIT HERE
    logs.write(m + "\n")
    
    if show==True:
        print m
        
    logs.close()

# Setting up initial parameters
immunity = [""]
handPicked = [""]
memberCap = 100
bannedSubs = [" "]
bannedUsers = ["PlaylisterBot", "AutoModerator", "PornOverlord", "Kebble", "Andrew-Mccutchen", "Threven"]
karmaDownLimit = 100  #minimum comment karma
karmaUpLimit = 100000000  #maximum comment karma
accountAgeLimit = 30 #minimum account age in days
wordsLimit = [" "]  #words we don't want in a username
recap = ""

#Variables for the crawler  UNUSED
#lastID = ""
#newID = ""



log("Signing in as NewTretkiBot...") #EDIT HERE

try:
    r = obot.login()
except:
    print "Wrong username/password combination"
else:
    s = praw.objects.Subreddit(r,"newtretki") #EDIT HERE
    log("Done")
	
# functions	
def kick(user):
    s.remove_contributor(user)
    flair(user,"[Kicked]",'kicked')
    log("Kicked " + user)
    
def add(user):
    s.add_contributor(user)
    log("Added " + user)
    
def getUserList(): 
    userList = []
    req = r.get_contributors("newtretki",limit=None) #EDIT HERE
    for u in req:
        username = str(u)
        if username != "NewTretkiBot": #EDIT HERE
            userList.append(username)
    userList.reverse()
    return userList

def flair(user,flair,css):
    s.set_flair(user, flair,flair_css_class=css)
    log("/u/"+user+"'s flair changed to '"+flair+"' (CSS "+css+")")

def postRecap(m):
    log("Posting the recap...")
    postTitle = str(today) +' - Bot Recap'
    r.submit("newtretki", postTitle, m).distinguish() #EDIT HERE
    log("Done")
  

#Kicking...
memberList = getUserList()
recap += "Kicked users:  \n"

log("Starting to kick inactive members...")

i = 0
n = 0

for member in memberList:
        i+=1
        log("#" + str(i) + " /u/" + member)

        if member in immunity:
                log("/u/" + member + " is in immunity list.")
                continue

        if member in handPicked:
                log("/u/" + member + " is in hand picked list.")
                continue

        overview = r.get_redditor(member).get_overview(limit=None)

        latestPost = 50000.0 #hours
        hoursLimit = 180.0 #hours

        for post in overview:
                postedSub = post.subreddit.display_name
                hoursAgo = (time.time()-post.created_utc)/3600.0

                if postedSub == "newtretki": #EDIT HERE
                        if hoursAgo < latestPost:
                                latestPost = hoursAgo
    
                if hoursAgo>hoursLimit:
                        break

        if latestPost <= hoursLimit:
                log("[OK] Latest post was " + str(latestPost) + " hours ago.")
        else:
                log("[NOT OK] No post in /r/newtretki in the last 7 days.") #EDIT HERE
                recap += "\#" + str(i) + " - /u/" + member + "\n\n"
                n+=1
                kick(member)

#Adding...      
comments = r.get_comments("all",limit=None)
nbAdded = memberCap-len(memberList)+n
newUser = ""
log("Adding " + str(nbAdded) + " users...")
newUser = ""
recap += "\nAdded users:  \n\n"

if nbAdded<0:
        nbAdded=0

while nbAdded>0:
        for c in comments:
                username = str(c.author)
                linkId = c.link_id.replace("t3_","")+"/"+c.id
                karma = c.author.comment_karma
                postedSub = c.subreddit.display_name
                accountAge = (time.time()-c.author.created_utc)/86400.0

                log("Considering /u/" + username + " from post " + linkId + ".")

                if username in bannedUsers:
                        log("[NOT OK] Banned user.")
                        continue
    
                if postedSub in bannedSubs:
                        log("[NOT OK] Posted in a banned subreddit")
                        continue

                if karma < karmaDownLimit:
                        log("[NOT OK] Comment karma too low.")
                        continue

                if karma > karmaUpLimit:
                        log("[NOT OK] Comment karma too high.")
                        continue

                if accountAge < accountAgeLimit:
                        log("[NOT OK] Account too recent.")
                        continue
    
                if any(word in username for word in wordsLimit):
                        log("[NOT OK] Username contains banned word.")
                        continue
                
                if random.randint(0,1) == 1:
                        log("[NOT OK] Not lucky enough.")
                        continue

                nbAdded-=1
                
                print nbAdded
                add(username)
                
                if newUser == "":
                        newUser = username

                if nbAdded==0:
                        break

#Change flairs...
new=""
i=0
for user in getUserList():
	i+=1
	if user==newUser:
		new="new"
   
	else:
		flair(user,'#'+str(i),'number'+new)
        
	if new=="new":
		recap += "\#" + str(i) + " - /u/" + user + "\n\n"
             

#Posting the recap...
postRecap(recap)