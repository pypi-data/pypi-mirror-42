# Paas-Word Django Authentication Middleware

[Paas-Word](https://www.paas-word.com) is an online authentication and user management service.
This Python Django middleware by [Paas-Word](https://www.paas-word.com) enables website owners with a Django backend to restrict their endpoints to authenticated users only and retrieve user data. 

## Usage

1. Create a free account at [Paas-Word](https://www.paas-word.com) website.
2. Recieve a login, sign-up, account and forgot-password pages for your website based on the user attributes you set up.
3. Set the callback pages on your website where users will be redirected after they sign-up and log in. 
4. Once a user is redirected to your website with a token, send this token to your backend in the "x-auth-token" header.

## Installation

Run:
```
    pip3 install paasword
```

Add "paasword" to settings.py :
```
    INSTALLED_APPS = [
        ...
        'paasword',
    ]
```

## Set Private Key as Environment Variable

Create an app on [Paas-Word](https://www.paas-word.com) and then set its Private Key as an environment variable on your server.

`export PAASWORD_APP_PRIVATE_KEY=93f56f52-957d-4953-93a6-c5492e79778b`

## Gaurd all endpoints

Add middleware to settings.py :
```
    MIDDLEWARE = [
        ...
        'paasword.middleware.Authenticate',
    ]
```

## Gaurd spesific routes against unauthenticated users

Remove comment from middleware.py. As an example:
```
if request.path.startswith('/snippets/'):
    return self.get_response(request)
```
    
## Retrieve user information

Call request.user
```
def snippet_list(request):
	if request.method == 'GET':
		print (request.user)
		snippets = Snippet.getAll()
		return JsonResponse(snippets, safe=False)
```