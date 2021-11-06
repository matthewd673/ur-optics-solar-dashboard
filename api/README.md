# Solar Dashboard Backend API

<https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials>

## Notes

* The official Box Python SDK is used for the authentication process, but not for other requests since it was throwing confusing errors.
So its only real purpose is to get us an `access_token` that can be used for manual requests.
* Currently, the `access_token` and `refresh_token` are stored in the Flask session (and can therefore be accessed from the frontend with a bit of work). This is a bad idea in terms of security, and should be changed later (see `store_tokens()`).
* Right now the API is essentially working under the assumption that nothing will go wrong, and doesn't have any sort of error handling. This is a WIP.

## .env
The server expects the following values to be found within `/api/.env` *(not tracked with Git)*.
They are all fairly self-explanatory
* `BOX_CLIENT_ID`
* `BOX_CLIENT_SECRET`
* `OAUTHLIB_INSECURE_TRANSPORT=1` *for testing on localhost only!*
* `MONGO_USERNAME`
* `MONGO_PASSWORD`
* `MONGO_DB` *the name of the specific database*

## Box Authentication

The following are used for OAuth2 authentication with Box. 
* `/box/get_auth_url`: send a user here to authenticate them. It will automatically redirect them to the appropriate Box sign-in page.
* `/box/auth_redirect`: the Box sign-in page redirects here once a user signs in. It double checks the tokens and then kicks them to `localhost:3000/` (TODO: give some sort of feedback).
* `/box/get_has_auth`: returns `"true"` if the session currently has a Box access token stored, and `"false"` otherwise. This is a pretty unsophisticated check, since if an access token goes bad we have no way of knowing.

## Box API Middleman Endpoints

There are a few endpoints that exist largely as a middleman for the Box API, sending along authentication data and simplifying the response.
* `/box/get_csv/<file_id>`: given the ID of a file in a Box account, return it as a `text/csv` file.
* `/box/get_folder_csvs/<folder_id>`: given the ID of a folder in a Box account, return a JSON list of the IDs of all CSV files.
* `/box/get_user_info`: returns the exact JSON output of [this Box endpoint](https://developer.box.com/reference/get-users-me/).
