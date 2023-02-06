# Social App Code_Graphers Test

## Project Description: 
This is social app in which user can signup, login,
Apply CRUD operations on posts and like the post

## Install and Run the Project: 
Clone the repository and install requirments.txt and project is ready to run.

## api:
there is an app name api in the project named social app
## Provided Urls: 

/registration : for register 
params: username, email, password

/login : for getting the JWT access and refresh token for user login
params: username , password

api/user: for get username information

api/token/refresh/ : for refresh the jwt tokken
params: refresh_token

api/posts : for all posts CRUD Operation, like and unlike 

request methods  | params in request body
---------------- | -------------
post             | title,body,author
get              | optional : userid(returns posts of specified user)
put              | required : pid(post-id), optional: title,body,likes,  unlikes
delete           | required: pid(post-id)

