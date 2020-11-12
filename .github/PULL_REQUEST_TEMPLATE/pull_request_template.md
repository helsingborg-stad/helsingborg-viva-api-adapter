## Explain the changes you’ve made
Good example: I've added support for authentication to implement Key Result 2 of OKR1. It includes model, table, controller and test. For more background, see #CLICKUP-ID.

## Explain why these changes are made
A good example: These changes complete the user login and account creation experience. See #CLICKUP_ID for more information.

## Explain your solution
A Good example: This includes a migration, model and controller for user authentication. I'm using Devise to do the heavy lifting. I ran Devise migrations and those are included here.

## How to test the changes?
Concrete example: Start the python development server.

## Screenshots (optional)
Backend code can benefit from a screenshot of the net change. This could be a comparission from one request to another or an imporved response.

## Anyhting else? (optional)
A good example: Let's consider using a 3rd party authentication provider for this, to offload MFA and other considerations as they arise and as the privacy landscape evolves. AWS Cognito is a good option, so is Firebase. I'm happy to start researching this path. Let's also consider breaking this out into its own service. We can then re-use it or share the accounts with other apps in the future.
