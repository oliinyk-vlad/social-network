1.Social Network
=======================
Launching:
```
python manage.py runserver
```

### Main endpoints

POST `/auth/jwt/create/` - obtain jwt token

GET `/activity/` - information about the activity of the current user

GET `/analytics/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD` - analytics about how many likes was made aggregated by day

**POSTS**

GET `/posts/` - get all posts

GET `/posts/{id}` - get post by id

POST `/posts/` - create post with  text which included in request body

POST `posts/{post_id}/{action}/` - like or dislike post

*_action_ - `like` _or_ `dislike`

*_all requests must be authenticated with Bearer token_




2.Automated bot
=======================
Parameters can be set in the file `config.json`

Launching:
```
python bot.py
```