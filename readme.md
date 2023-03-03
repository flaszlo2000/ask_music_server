## TODO
- postgres db connection on default but if it fails then get backup from sqlite
    - [x] script that capable to make backup from postgres
    - [] detect postgres fail
    - [] on postgres fail, try to restore it from sqlite, if it is not possible then switch to sqlite and send somekind of notification
        - [] send notification 
- send record request from admin to a event that is not ongoing
- record blacklist
- delete record


# deploy
You will need 2 things: 
- `ENV_FILE_PATH`: to be able to find env file. This is handy because on local/dev server you can use local .env files and on deploy, by setting secret environment variables you can access the real settings.
You will need something like this:
```
DATABASE_URL="driver://access_to_db"
ALLOW_ORIGINS=...
ALLOW_CREDENTIALS=...
ALLOW_METHODS=...
ALLOW_HEADERS=...
```
See more on fastapi docs.
- `SERVICE_WORKERS`: To set how many service workers should the server start

On real deploy, I recommend to use server.sh to start the service, but on dev run.sh was prefferred by me.