## TODO
- postgres db connection on default but if it fails then get backup from sqlite
    - [x] script that capable to make backup from postgres
    - [] detect postgres fail
    - [] on postgres fail, try to restore it from sqlite, if it is not possible then switch to sqlite and send somekind of notification
        - [] send notification 
- send record request from admin to a event that is not ongoing
- record blacklist
- delete record
- jwt renewal
- db indexing ?


# deploy
You will need these things: 
- `ENV_FILE_PATH`: to be able to find env file. This is handy because on local/dev server you can use local .env files and on deploy, by setting secret environment variables you can access the real settings.
You will need something like this:
```
DATABASE_URL="driver://access_to_db"

ALLOW_ORIGINS=...
ALLOW_CREDENTIALS=...
ALLOW_METHODS=...
ALLOW_HEADERS=...

JWT_ALGORITHM=...
JWT_EXPIRE_MINS=...
```
See more on fastapi docs.
- `SERVICE_WORKERS`: To set how many service workers should the server start
- `DB_BACKUP_STRATEGY`: This should be 0/1, see db_backup.py's `DATA_BACKUP_STRATEGIES`
- `JWT_SECRET_KEY`: **very** secret key to encode JWT's

On real deploy, I recommend to use server.sh to start the service, but on dev run.sh was prefferred by me.

## This project features two-factor authentication
It's been implemented via webhooks with the following process stream:  
`/maintainer/token -> /maintainer/2f_auth/send_code -> /maintainer/2f_auth/login`  

- `/maintainer/token`: normal oauth2 login that will grant an option (jwt with special scope) to send a two-factor code and login with it in a time limit
- `/maintainer/2f_auth/send_code`: with the special jwt, the webhook call can be fired here
- `/maintainer/2f_auth/login`: waits for the special jwt and the two-factor code

To be able to use this you have to provide an a variable called `INITIAL_WEBHOOKS_2F_URL` in your `.env` file for the first startup or manually add a maintainer admin record with `webhooks_url` field in the project's existing db. 
At startup the program will automatically lookup into the `.env` if the data is not present in the db, then if it finds it in there, will save it for further use.

When first started, and there is no maintainer level admin in the db (who could register anyone), the program is going to generate a random user and send it's password to the provided webhook url in the `.env`.