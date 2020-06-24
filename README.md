# how_i_meet_your_better

*This site will allow anyone to find a healthy substitute for a food considered "Too fat, too sweet, too salty"*

## Behavior driven development :
### 1/ Research of best food :
**As a** customer \
**I want** to search for a food product on the site\
**In order to** to find a healthier substitute for the foods i usualy eat

### look_for_healthier_food :
**Given** a customer wants to search for a healthier food substitute \
**When** it will enter the original product in the search box on the home page \
**Then** the site performs a comparison of foods \
**And** offers the substitute with the best nutriscore in a dedicated product page


### display_best_product :
**Given** a customer want consult detail on a best product \
**When** he become in the detail page product\
**Then** he can view all the details of the best product
**And** see the comparison with the original product

### record_food_substitute_found :
**Given** a user has found a substitute food (he is on the food substitute detail page)\
**And** he wants to save it \
**When** he clicks on the save button \
**Then** the system save the article in the favorite food substitute \
**And** the user stay in the same detail product page

### 
**Given** \
**When** \
**Then**

### 2/ Create and consult your account :
**As a** customer \
**I want** i want to be able to create an account \
**In order to** be able to use the site, save my preferences and consult them

### create_your_account :
**Given** as a user wanting to use the application \
**When** i fill in the account creation form with my email and password \
**And** i accept the conditions of use of the website \
**Then** the website saves my information in the database \
**And** sends me back to the home page of the site

### connection_to_your_account :
**Given** a user who has created an account wants to authenticate \
**When** he enters his email and password \
**Then** the system will verify that the email and password exist and are correct
**And** return the user to the home page


### consult_your_data :
**Given** a connected user wants consult their data \
**When** he will click on "my profil" tab
**Then** the system will redirect the user to their profile page

## DATA

**USER** (<ins>id_user</ins>, email, password)  
**FAVORIS** (<ins>_id_user_</ins>, <ins>_code_product_</ins>, id_favoris)  
**PRODUCT** (<ins>code_product</ins>, product_name, nutriscore)  
**PRODUCT_CATEGORY** (<ins>_code_product_</ins>, <ins>_id_category_</ins>, id_product_category)  
**CATEGORY** (<ins>id_category</ins>, category_name)