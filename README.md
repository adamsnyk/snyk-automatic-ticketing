# Snyk Automatic Ticketing

If you do not have a Jira board but want automic ticketing for new issues - we got your back!

This project let's you publish yesterday's vulns to ANY ticketing board that you use. Assuming they have a Rest API.

## Setup

### 1. Fork this Project

You'll need to fork and edit this repo for yourself to make the last "publish ticket" API call work.

### 2. Get your Snyk Token & Org ID 

Your Snyk Token authenticates every Snyk API call.

Your Org ID specifies which Org to filter issues for.

Get these two values, then set `SNYK_TOKEN` and `SNYK_ORG` as Python env-vars, respectively.

### 3. Deploy to Heroku

You can sync Heroku with a GitHub Repo through their website. Should take 2 minutes without coding.

Also, set `SNYK_TOKEN` and `SNYK_ORG` in Heroku > Settings > Config Vars.

### 4. Setup a Scheduler

Setup a cheduler in Heroku > Recources > Find Add-ons > Heroku Scheduler > add job.

You need a C.C. but it's free to setup.

Your job should run `python scripts/publish_new_vulns.py` and set schedule to `once per day`.

### TODO: Complete your publish API call

This boilerplate project just runs `pprint` on yesterday's issues. If you want them on your board, figure out your board's Rest API and add the final `requests.post(...)` call.

Then you should be good to go!