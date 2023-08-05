# API Reference
How to use the `repltalk` lib for Python. The functions are pretty self explanatory but I've added a short description for each of them.
## Client
`class repltalk.Client()`

*The following functions are all coroutines*
+ `login(username, password)`
Logs in to Repl.it with your username and password. Your bot must be verified in order to use this function.
*returns None*
+ `get_post(post_id)`
Gets the post with that id.
*returns Post*
+ `get_leaderboard(limit=30)`
Gets the top users from the Repl Talk leaderboard.
*returns list of `User`s*
+ `get_all_comments()`
Gets all the recent comments from Repl Talk.
*returns list of `Comment`s
+ `get_user(username)`
Gets the user with that username.
*returns User*

+ `boards`
See *Board*.
***
## Board
`class client.board`

+ `all`
The *All* board on Repl Talk
+ `share`
The *Share* board on Repl Talk
+ `ask`
The *Ask* board on Repl Talk
+ `announcements`
The *Announcements* board on Repl Talk
+ `challenge`
The *Challenge* board on Repl Talk
+ `learn`
The *Learn* board on Repl Talk
***
+ `get_posts()`
Gets the most recent posts from that board.
*returns list of `Post`s*

## Post
+ `id`
The post ID
+ `title`
The post title
+ `content`
The post content
+ `board`
The board the post was made on.
+ `votes`
The amount of upvotes the post has.
+ `author`
The post author. Will be a User object.
+ `datetime`
The time the post was created at.
+ `url`
The post url in Repl Talk.
+ `repl`
The repl attached to the post.
+ `show_hosted`
Indicates if the post has a hosted repl linked to it.
+ `is_announcement`
If the post is marked as an announcement.
+ `can_edit`
Indicates if the user can edit the post. This will be *False* unless you created the post.
+ `can_comment`
If the user can comment on the post.
+ `can_vote`
Indicates if the user can upvote the post.
+ `has_voted`
Indicates if the user has already voted on the post.
+ `is_locked`
Indicates if the post is locked.
***
+ `get_comments()`
Gets the comments on the post.

## Comment
+ `id`
The post ID.
+ `content`
The post body.
+ `time_created`
The time the comment was created at.
+ `can_edit`
Indicates if the user can edit the comment.
+ `can_comment`
Whether or not the user can post a comment.
+ `url`
The comment's url.
+ `votes`
Gets the amount of upvotes the comment has.
+ `can_vote`
Indicates if the user can vote on the comment.
+ `has_voted`
Indicates if the user has already upvoted the post.

## User
+ `id`
The user ID. Pretty useless since you can't get the user from their id.
+ `name`
The user's username.
+ `avatar`
The user's avatar url
+ `url`
The user's profile link
+ `cycles`
The amount of cycles that user has
+ `roles`
The roles the user has set on their profile.