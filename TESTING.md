## Manual Testing

Manual testing implemented for the Back-End application listed below:


|     | User Actions           | Expected Results | Y/N | Comments    |
|-------------|------------------------|------------------|------|-------------|
| **APPS**     |
| **Profiles**     |                        |                  |      |             |
| 1           | Logged-in user enters profiles URL | Profile List renders all profiles as array of objetcs. User cannot create profile, only list view available | Y |          |
| 2           | Profile owner enters profile's detailed url with existing PK | Renders profile's details in the browser, is_owner property is set to true, user can update details with form and submit with PUT method | Y |          |
| 3           | Form fields format validation | Correct input format required from user | Y |          |
| 4           | Submit signup with blank fields | Form validation triggered, highlight the field, submission aborted | Y |          |
| 5           | Submit signup with correct values | Account Inactive site displayed | Y |      Email send/receive tested with real email account    |
| 6           | Sign in link in the header message | Redirects to login page | Y |          |