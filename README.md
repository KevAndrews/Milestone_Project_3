<h1 align="center">Game Reviews</h1> 
The scope for this project is to create a user centric website using Flask, Python, MongoDB and Heroku.
<br/><br/>
Game Reviews is a website that allows users to search for Games that they would like to play and see what the community has to say. You can join the community and add to the growing selecting of games and review.
<br/><br/>

![Responsive displays](images/responsive.png)

# Table of contents
- [UX](#user-experience)
    - [User stories](#user-stories)
    - [Design](#design)
    - [Surface Plane](#surface-plane)
    - [Wireframes](#wireframes)
- [Technologies Used](#technologies-used)
    - [Languages and Frameworks](#languages-and-frameworks)
- [Code Validation](#code-validation)
- [Database Schema](#database-schema)
- [Database](#database)
    - [MongoDB Setup](#mongodb-setup)
- [Deployment](#deployment)
    - [Forking the GitHub Repository](#forking-the-github-repository)
    - [Making a Local Clone](#making-a-local-clone)
    - [Heroku Deployment](#heroku-deployment)
- [Credits](#credits)
- [Content](#content)
- [Acknowledgements](#acknowledgements)


# User Experience
## User stories
## Design
## Surface Plane
## Wireframes

# Technologies Used
## Languages and Frameworks
- [Python](https://www.python.org/)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [HTML](https://en.wikipedia.org/wiki/Hypertext_Markup_Language)
- [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
- [Materializecss](https://materializecss.com/)
- [Fontawesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)
- [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))
- [JQuery](https://jquery.com/)


# Code Validation
- [W3 HTML Validator](https://validator.w3.org/) 
- [W3 CSS Validator](https://jigsaw.w3.org/css-validator/)
- [JShint](https://jshint.com/)
- [PEP8 checker](http://pep8online.com/)

# Database Schema

# Database

## MongoDB Setup
1. Sign up for a free account and login to [MongoDB](https://www.mongodb.com).
2. (If you are new at MongoDB) create a cluster first by clicking "Create" and following the steps.
3. Go to your cluster and click on the button "Connect".
4. Select "Connect to your application".
5. Select Python as "Driver" and choose "Version 3.6 or later"
6. Use the below collection schema

![Responsive displays](readme_images/responsive.png)

# Deployment

## Forking the GitHub Repository
The GitHub Repository can be forked to make a copy of the original repository on the GitHub account to view and/or make changes without affecting the original repository in the following way.

1.	By logging in to GitHub and locating the [GitHub Repository](https://github.com/KevAndrews/Milestone_Project_3).
2.	Selecting the "Fork" button at the top of the Repository (it is located at the top right of the page under the profile image).
3.	There should then be a copy of the original repository in your GitHub account.

## Making a Local Clone
The GitHub Repository can be cloned in the following way:

1.	By logging in to GitHub and locating the [GitHub Repository](https://github.com/KevAndrews/Milestone_Project_3).
2.	Under the repository name, clicking the dropdown button marked “Code” and then selecting "Clone or download".
3.	Copying the link under "Clone with HTTPS", to clone the repository using HTTPS.
4.	Opening Git Bash.
5.	Changing the current working directory to the location where you want the cloned directory to be made.
6.	Typing git clone, and pasting the URL copied in Step 3.
7.	Pressing Enter to create the local clone.

## Heroku Deployment
1. For Heroku first create a requirements.txt file by running the following command in the CLI:
    - **pip3 freeze --local > requirements.txt**
2. Create a Procfile file with this command:
    - **echo web: python app.py > Procfile**
3. Sign up and log in to [Heroku](https://www.heroku.com/).
4. Create a new app by clicking on the button "New".
5. Give your app a name, select your region and click "Create app".
6. Navigate to the "Deploy" tab and select "Github" as a deployment method.
7. Search for your repository name and connect.
8. Now open the "Settings" tab and click on "Reveal Config Vars".
9. Add your configuration variables:
    - **IP** : `0.0.0.0`
    - **PORT** : `5000`
    - **SECRET_KEY** : `<secret_key>`
    - **MONGO_URI** : `<mongodb_URI>`
    - **MONGO_DBNAME** : `<db_name>`
10. Navigate to the Tab "Deploy" and enable "Automatic Deploys".

# Credits

1.	https://www.favicon.cc/?action=icon&file_id=520466
2.	https://wallpaperaccess.com/80s-retro-games

# Content
The audio and images belong to documented third parties noted in Credits section above, all other content was written by the developer.

# Acknowledgements
I would like to thank the team at the Code Institute for all the courses they provided that help me gain the knowledge I needed to build this game.
<br/><br/>
I would also like to thank my wife Áine for her support throughout its development.