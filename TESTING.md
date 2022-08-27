## Manual Testing

Manual testing implemented for the Back-End application listed below:


|     | User Actions           | Expected Results | Y/N | Comments    |
|-------------|------------------------|------------------|------|-------------|
| **APPS**                                                                          |
| **Profiles**     |                        |                  |      |             |
| 1           | Logged-in user enters profiles URL | Profile List renders all profiles as array of objetcs. User cannot create profile, only list view available | Y |    Profile creation is handled by django-signals      |
| 2           | Profile owner enters profile's detailed url with existing PK | Renders profile's details in the browser, `is_owner` property is set to `true`, user can update details with form and submit with `PUT` method. **DELETE** button is visible. | Y |   Form fields are populated with fetched profile data.       |
| 3           | User clicks **DELETE** button | Profile is deleted. User is redirected to Profile List view. The deleted profile is not displayed. User instance is destroyed with django-signals. | Y |       |
| 4           | The user enters profile's detailed url which he does not own with existing PK | Renders profile's details in the browser, `is_owner` property is set to `false`, update form is not displayed. The **DELETE** button is not visible. | Y |          |
| 5           | Profile owner change data and submits with `PUT` button | The updated profile detail view is rendered. Data is saved in the database. | Y |          |
| 6           | Filters: User selects product in the field filters | List all profiles which owner's give rating to the selected product  | Y |   DRF known bug for `[invalid name]` present    |
| 7           | Filters: User selects ordering by products_count ascending  | List of all profiles is displayed sorted by products_count in asceding order | Y |          |
| 8           | Filters: User selects ordering by products_count descending  | List of all profiles is displayed sorted by products_count in descending order | Y |          |
| 9           | Filters: User selects ordering by ratings_count ascending  | List of all profiles is displayed sorted by ratings_count in asceding order | Y |          |
| 10           | Filters: User selects ordering by ratings_count descending  | List of all profiles is displayed sorted by ratings_count in descending order | Y |          |
| 11           | Filters: User selects ordering by comments_count ascending  | List of all profiles is displayed sorted by comments_count in asceding order | Y |          |
| 12           | Filters: User selects ordering by comments_count descending  | List of all profiles is displayed sorted by comments_count in descen ding order | Y |          |
| **Products**     |                        |                  |      |             |
| 1           | Logged-in user enters products URL | Product List renders all products as array of objetcs. User can create product in the form rendered in the browser. | Y |          |
| 2           | Logged-in user fills all required fields in the Product form and clicks `POST` button | The submitted product is displayed in the browser and database is updated. | Y |          |
| 3           | Logged-in user does not fill all required fields in the Product form and clicks `POST` button | The required field is highlihted, user is prompted that the field cannot be blank | Y |          |
| 4           | Logged-in user does not fill all required fields in the Product form and clicks `POST` button | The required field is highlihted, user is prompted that the field cannot be blank | Y |          |
| 5           | Product owner enters product's detailed url with existing PK | Renders product's details in the browser, `is_owner` property is set to `true`, user can update details with form and submit with `PUT` method. **DELETE** button is visible. | Y |   Form fields are populated with fetched product data.       |
| 6           | User enters product's detailed url which he does not own with existing PK | Renders product's details in the browser, `is_owner` property is set to `false`, update form is not displayed. The **DELETE** button is not visible. | Y |          |
| 7           | Product owner change data and submits with `PUT` button | The updated product detail view is rendered. Data is saved in the database. | Y |          |
| 8           | Filters: User selects owner in the field filters | List all products of the selected owner  | Y |      |
| 9           | Filters: User selects InStock boolean value in the field filters  | List all products with selected value | Y |          |
| 10           | Filters: User selects Category value in the field filters  | List all products with selected category | Y |          |
| 11           | Filters: User types existing Brand name in the field filters  | List all products with specified Brand | Y |          |
| 12           | Filters: User selects ordering by price ascending  | List of all products is displayed sorted by price in asceding order | Y |          |
| 13           | Filters: User selects ordering by price descending  | List of all products is displayed sorted by price in descending order | Y |          |
| 14           | Filters: User selects ordering by avg_score ascending  | List of all products is displayed sorted by avg_score in asceding order | Y |          |
| 15           | Filters: User selects ordering by avg_score descending  | List of all products is displayed sorted by avg_score in descending order | Y |          |
| 16           | Filters: User selects ordering by all_scores ascending  | List of all products is displayed sorted by all_scores in asceding order | Y |          |
| 17           | Filters: User selects ordering by all_scores descending  | List of all products is displayed sorted by all_scores in descending order | Y |          |
| 18           | Filters: User selects ordering by title ascending  | List of all products is displayed sorted by title in asceding order | Y |          |
| 19           | Filters: User selects ordering by title descending  | List of all products is displayed sorted by title in descending order | Y |          |
| 20           | Filters: User selects ordering by created_at ascending  | List of all products is displayed sorted by title in created_at order | Y |          |
| 21           | Filters: User selects ordering by created_at descending  | List of all products is displayed sorted by created_at in descending order | Y |          |
| 22           | Filters: User types existing user's username in the searchbar  | List of all products is displayed that matches username search query | Y |          |
| 23           | Filters: User types existing product's title in the searchbar  | List of all products is displayed that matches product's title search query | Y |          |
| 24           | Filters: User types keyword to be seareched in the product's descritpion in the searchbar  | List of all products is displayed that matches keyword in products desriptions search query | Y |          |
| **Comments**     |                        |                  |      |             |
| 1           | Logged-in user enters comments URL | Comments List renders all comments as array of objetcs. User can create comment in the form rendered in the browser. | Y |          |
| 2           | Logged-in user fills all required fields in the Comment form and clicks `POST` button | The submitted comment is displayed in the browser and database is updated. | Y |          |
| 3           | Logged-in user does not fill all required fields in the Comment form and clicks `POST` button | The required field is highlihted, user is prompted that the field cannot be blank | Y |          |
| 4           | Comment owner enters comment's detailed url with existing PK | Renders comment's details in the browser, `is_owner` property is set to `true`, user can update details with form and submit with `PUT` method. **DELETE** button is visible. | Y |   Form fields are populated with fetched comment data.       |
| 5           | User enters comment's detailed url which he does not own with existing PK | Renders profile's details in the browser, `is_owner` property is set to `false`, update form is not displayed. The **DELETE** button is not visible. | Y |          |
| 6           | Comment owner change data and submits with `PUT` button | The updated comment detail view is rendered. Data is saved in the database. | Y |          |
| 7           | Filters: User selects Comment in the field filters | List all comments of the selected Comment  | Y |      |
| 8           | Filters: User selects Owner in the field filters  | List all comments with selected Owner | Y |          |
| **Ratings**     |                        |                  |      |             |
| 1           | Logged-in user enters ratings URL | Ratings List renders all ratings as array of objetcs. User can create rating in the form rendered in the browser. | Y |          |
| 2           | Logged-in user fills all required fields in the Rating form and clicks `POST` button | The submitted rating is displayed in the browser and database is updated. | Y |   All fields are choice fields with default value - no blank       |
| 4           | Rating owner enters rating's detailed url with existing PK | Renders rating's details in the browser, `is_owner` property is set to `true`, user can update details with form and submit with `PUT` method. **DELETE** button is visible. | Y |   Form fields are populated with fetched rating data.       |
| 5           | User enters rating's detailed url which he does not own with existing PK | Renders profile's details in the browser, `is_owner` property is set to `false`, update form is not displayed. The **DELETE** button is not visible. | Y |          |
| 6           | Rating owner change data and submits with `PUT` button | The updated rating detail view is rendered. Data is saved in the database. | Y |          |
| 7           | Filters: User selects Rating in the field filters | List all ratings of the selected Rating  | Y |      |
| 8           | Filters: User selects Owner in the field filters  | List all ratings with selected Owner | Y |          |