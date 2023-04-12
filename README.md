

## Installing dependencies

In order to run this Flask app, activate the virtual environment of your choice, then run:

`
pip install -r requirements.txt
`

This will install all the requirements needed to run the Flask app.

In order to actually run the app, navigate to the base repository directory. Your current directory should contain main.py. Run the following:

`
flask --app main run
`

The command line will output the port on which the website is running.

## Uploading files

CSV files can be uploaded from the path `"/upload"`. An uploaded file will be automatically parsed and ingested into the database. In order for the file to be properly parsed and inserted, the following conventions must be followed:

- The filename must be in `{"user.csv", "nutrition.csv"}, or of the form{ "recovery.'name'.csv", "sleep.'name.csv", "hawkins.'name.csv"}`. Uploaded files currently overwrite the previous csv of the same name; this should be changed in a later version.
- The csv file must contain the correct column labels.

# CS321-Milestone5
<h2>Deployment to Cloud</h2>

### Abstract: 
This milestone involved developing a dynamic version of our Athletic Management System to the cloud.  We relied on our work from Milestone 4 (Flask website) as a base for adding new functional features from our backlog.  This included using biometric data (and updating our graphs and tables to reflect this), and deploying our app to the cloud.  Our plan was (in the form of issues) as follows:
* Host the app on the cloud
* Use real data in the data base
* Refactor the format of our HTML files 
* Add fields to database objects
* Aggregate our data
* Use real data in our graphs and tables
* Revamp our sign up functionality


### Sprint Backlog:
#### User stories (general):
<p> update this once milestone is completed </p>
<p>As a user I can create a new account using an email and password – Completed<br>
As a user of the website I can log in to the website with a username and password – Completed<br>
As a user of the website I can login to my assigned role –Completed<br>
As a user of the website, I can navigate back to my dashboard by clicking on the mule icon – Partially completed (works for moving between athlete detail pages and dashboard)</p>

#### Admin/Peak:
<p>As an admin, I can log in with user name and password -  completed<br>
As an admin, after logging in I can navigate to my dashbord -  completed<br>
As an admin, I can view my dashbord on the website - completed<br>
As an admin, I can view all of the sports teams in the teams table - completed <br>
As an admin, I can edit one file (TeamNames.csv) to change what teams appear on my dashboard - completed<br>
As an admin, when I click on a team name I will be redirected to the associated team view page - completed<br>
As an admin, on my team view pages, I can see team name, team data, and a list athletes of that team - completed<br>
As an admin, when on team view, I can click on an athlete's name and be redirected to the corresponding athlete view page - complete<br>
As an admin, on my view of athletes, I can see their name, their sports science data, and important notes about the athlete - complete at a basic stage
(all athletes have same data)<br> 
</p>

#### Athlete:


#### Coach



### Results: 
<img width="1000" alt="Screen Shot 2022-11-09 at 10 13 35 PM" src="https://user-images.githubusercontent.com/30237570/200992076-42d2d240-6ee6-4633-823a-02f36a289872.png">
Updated graphs (as shown in athlete dashboard) illustrating real data from our database.

Admin Views: (in order) Dashboard, Team view, Athlete view
<img width = "1000" src = "https://user-images.githubusercontent.com/113453620/201239056-b402fd8e-fefc-4203-9212-148b793bf394.png">
<img width = "1000" src ="https://user-images.githubusercontent.com/113453620/201239357-e14a083f-ec3f-4188-817e-7734b138731e.png">
<img width = "1000" src = "https://user-images.githubusercontent.com/113453620/201239424-175d86d6-3c6c-49db-b15c-f678593031fa.png">



### Burn Down Chart:
![image](https://user-images.githubusercontent.com/70499767/201227693-4671b947-abd1-4442-88c2-5338610a85f5.png)


### Team Reflection: 


### Contribution List: 
* Calvin: Reformatted the data classes in models.py and reviewed pull requests to resolve conflicts in merging. Created the burndown chart for this milestone.
* Matt: Worked on parsing csv files into objects in our database with parameters for each of the columns.
* Ben: Worked on setting up flask security and email confirmation/password reset
* Hannah: Worked on fixing bugs in permissions.
* Milo: Added a config file and a secret key to the repo to enable cloud deployment. Configured a free account and webapp service on Microsoft Azure to enable cloud hosting of our application. Helped troubleshoot with other developers and took the lead on reviewing pull requests.
* Tamsin: connected database to plotly graphs, reconstructed subplots to individual graphs & made appropriate edits in HTMl dashboard files
* Nicole: 


### Extensions: 
We added a functional ReadMe file to our repository detailing the website.

### References: 
Naser Al Madi


# CS321-Milestone6
<h2>CI/CD Testing</h2>

### Abstract: 
This milestone involved developing  a CI/CD pipeline to lint, test, and deploy a dynamic version of our Athletic Management System to the cloud.  The updates made to our Flask website in this milestone build on top of the previous milestone (Milestone 5), and add tests along with new functional features from our backlog. 

### Burn Down Chart:
![image](https://user-images.githubusercontent.com/70499767/203463894-b320b703-75f4-4ac1-8064-d4b713cb1b0e.png)


### Team Reflection: 
<p>

This week we worked on our communication and by the latter half of the milestone we made some good progress. Our issues we made sure to be smaller so that each team member was able to make progress on a number of individual issues. Our meeting to get our develop branch working took longer than it should have because we didn't fully respect every team member's ideas. We also had two team members leave our group without making clear that they had which made finishing the issues they were assigned much more difficult. 
</p>



### Sprint Backlog:
#### User stories (general):
<p> As a user I can login with my email and password - completed </p>

#### Admin/Peak:
<p>  
As an Admin I can view the averages of all of the athletes' data - completed </br>
As an Admin I can see a breakdown of all of the teams' average data - completed </br>
As an Admin I can add new users -  partially complteded, anyone can do this through the upload file but adding a user in the permissions page does not fully work </br>
</p>

#### Athlete:
<p> 
As an Athlete I can view my recent data - completed </br>
As an Athlete I can view a history of my data - partially completed, only readiness is shown </br>
</p>

#### Coach
<p>
As a coach I can view data on my team as a whole - completed</br>
As a coach I can see my athlete's breakdowns for my team - completed </br>
As a coach I can click on an athlete and see their specific data - completed </br>
</p>


### Results: 


### Contribution List: 

* Calvin: Reviewed and resolved pull requests, wrote (but not finished at time of sprint-end) functional tests for athlete data views on nutrition, readiness, and sleep quality. Created the burndown chart.
* Matt: Added continuous integration. Made permissions page more accurate. Made admins be able to view all of the teams and their data averages. Added functinality to coach's view to see athletes of their team and the athletes' data. Worked on setting up a functional database. Added function to populate empty database. Was scrum master for this Milestone.
* Ben: 
* Milo: Wrote several functional & unit tests. Deployed the website to the web publicly, and created another develop deployment slot for testing.
* Tamsin: wrote code to pull database data into ``views.py`` for use in adminView, teamView, and athleteView graphs, fixed general CSS layout bugs throughout the website, edited HTML redirects to appropriate data view pages


### Extensions: 
We added a functional ReadMe file to our repository detailing the website.

### References: 
Naser Al Madi

# CS321-Milestone7
<h2>API Integration</h2>

### Abstract: 
This milestone involved researching APIs to pull data from wearable devices into our app.  An API is a set of functions and procedures allowing the creation of applications that access the features or data of an operating system, application, or other service.  We focused on the Google Drive API and learned a lot from the example we went over in class last week.  

### Burn Down Chart:
![image](https://user-images.githubusercontent.com/70499767/206769461-efc745ac-e992-4b4b-9a0f-e4c8c4d6f304.png)


### Team Reflection: 
<p>
We continued implementing our goals in the form of smaller issues and assigned these issues early on so that it was clear what was expected of each team member during the milestone.  Our testing practices also improved during this milestone, and our communication via pull requests and Git comments was good.  This week, we split assignments and time between working on integrating the APIs, developing new features, and fixing bugs from previous milestones.  We hope to improve our work and add even more functional features for the version submission of our system.  We also experienced some difficulty this week due to our Azure subscription being discontinued.  We had to rush to start moving things over to Heroku at the last minute, so this project is still a work in progress. 
</p>


### Sprint Backlog:
#### User stories (general):
<p> As a user I can login with my email and password - completed </p>

#### Admin/Peak:
<p>  
As an Admin I can view the averages of all of the athletes' data - completed </br>
As an Admin I can see a breakdown of all of the teams' average data - completed </br>
As an Admin I can add new users -  completed </br>
As an Admin I can remove users -  completed </br>
</p>

#### Athlete:
<p> 
As an Athlete I can view my recent data - completed </br>
As an Athlete I can view a history of my readiness data - completed</br>
</p>

#### Coach
<p>
As a coach I can view the averages of all of my team's data - completed </br>
As a coach I can see a breakdown for each individual athlete on my team - completed </br>
As a coach I can view a history of my team's readiness data data - completed</br>
</p>


### Results: 
<p> login screen: </p
<p> <img width="1438" alt="Screen Shot 2022-12-09 at 10 06 11 AM" src="https://user-images.githubusercontent.com/30237570/206731905-6c55a0bd-0154-42ac-8b12-4b87a5773b0b.png"> </p>

<p> admin dashboard: </p>
<p> <img width="1429" alt="Screen Shot 2022-12-09 at 10 07 03 AM" src="https://user-images.githubusercontent.com/30237570/206732105-4e5b46b4-7506-488c-8a6b-933492e872e8.png"> </p>

<p> permissions dashboard: </p>
<p><img width="1423" alt="Screen Shot 2022-12-09 at 10 10 43 AM" src="https://user-images.githubusercontent.com/30237570/206732809-6f91b55d-861f-4f27-b428-05f8d02fdb8e.png">
 </p>
 
<p> add users: </p>
<p> <img width="1429" alt="Screen Shot 2022-12-09 at 10 11 15 AM" src="https://user-images.githubusercontent.com/30237570/206732941-344c5ca3-afc2-42b1-a4b8-41d1b2ed6e32.png"> </p>

<p> remove users: </p>
<p><img width="1433" alt="Screen Shot 2022-12-09 at 10 11 52 AM" src="https://user-images.githubusercontent.com/30237570/206733056-38b57ce5-6c63-4b49-b550-fc1493513f32.png">
 </p>

<p> upload data (admin only): </p>
<p><img width="1424" alt="Screen Shot 2022-12-09 at 10 12 17 AM" src="https://user-images.githubusercontent.com/30237570/206733137-659cfe05-a788-4e5a-a7b0-6926c6453a96.png">
 </p>
 
 <p> improved methods of switching between teams (search bar and dropdown menu): </p>
 <p><img width="772" alt="Screen Shot 2022-12-12 at 6 18 56 PM" src="https://user-images.githubusercontent.com/30237570/207180560-5b83f695-975c-4ebc-99c9-0fc58e3c4192.png">
 </p>
 <p><img width="339" alt="Screen Shot 2022-12-12 at 6 19 02 PM" src="https://user-images.githubusercontent.com/30237570/207180571-9b7ecf55-5d0f-4f8c-94f3-f72d4bd281f3.png">
 </p>

<p> coach dashboard: </p>
<p><img width="1428" alt="Screen Shot 2022-12-12 at 6 18 32 PM" src="https://user-images.githubusercontent.com/30237570/207180514-0c32ee17-531e-452e-a761-7840ce5e7da6.png">
 </p>

<p> athlete dashboard: </p>
<p><img width="1430" alt="Screen Shot 2022-12-12 at 6 18 45 PM" src="https://user-images.githubusercontent.com/30237570/207180502-eb38d2a0-dc5d-43fa-b6fe-c22c403f8bf8.png">
 </p>


### Contribution List: 
* Calvin: Implemented more tests to increase test coverage and ensure quality code. Created both funtional and unit tests, and added the burndown chart.
* Matt:
* Ben: 
* Milo: Implemented Google Drive API capabilities.
* Tamsin: scrum master, wrote and assigned new issues, researched Google Drive, MyFitnessPal, Oura Ring, Hawkins, and FitBits Apis, improved documentation, implemented a dropdown menu in the dashboard header to allow users with multiple teams to switch between their teams, made slides to introduce project presentation
* Anton: 


### Extensions: 
* Functional ReadMe file to our repository detailing the website.
* Extensive documentation in all files to improve coherence.
* Implemented functionality to remove users.
* Implemented functionality to send login recovery emails for improved security.
* Added more UI features for increased accessibility (search bar, dropdown menu to switch between teams)


### References: 
Naser Al Madi

# CS321-Milestone8
<h2>Refactoring & Better Design </h2>

### Abstract: 
This milestone involved refactoring and enhancing the quality of our software by focussing on design patterns and anti-patterns.  We implemented  remaining items in our product backlog and refactored our code to enhance readability and maintainability.  We strove to implement multiple APIs, maintain a test coverage above 90%, and reduce the complexity of our code by refactoring it (as measured by code metrics).  This milestone also involved the use of Radon (a Python tool for calculating code metrics) to calculate Cyclomatic Complexity and Maintainability Index for our code before and after refactoring, with the “before” calculations being from the repository submitted for Milestone 7.

### Burn Down Chart:
<p>
<p> <img width="1000" alt="Burndown Chart 8" src="https://user-images.githubusercontent.com/70499767/208593734-867662c6-9322-4288-be2d-f35a992dab5e.png"> </p>

</p>


### Team Reflection: 
<p>

</p>


### Sprint Backlog:
#### User stories (general):
<p> As a user I can login with my email and password - completed </p>
<p> As a user I can use my email for account recovery - completed </p>

#### Admin/Peak:
<p>  
As an Admin I can view the averages of all of the athletes' data - completed </br>
As an Admin I can see a breakdown of all of the teams' average data - completed </br>
As an Admin I can add new users -  completed </br>
As an Admin I can remove users -  completed </br>
</p>

#### Athlete:
<p> 
As an Athlete I can view my recent data - completed </br>
As an Athlete I can view a history of my readiness data - completed</br>
</p>

#### Coach
<p>
As a coach I can view the averages of all of my team's data - completed </br>
As a coach I can see a breakdown for each individual athlete on my team - completed </br>
As a coach I can view a history of my team's readiness data data - completed</br>
</p>


### Results: 
<p> Radon results before refactoring: </p
<p> <img width="1125" alt="Screen Shot 2022-12-18 at 9 39 40 PM" src="https://user-images.githubusercontent.com/30237570/208337158-86cf07da-aa60-4383-b2e7-17742b85983e.png"> </p>
<p> Radon results after refactoring: </p>
<p> Latest commit number: 214cb3a1695f3d94b0335d2f5fe1ab498451ddd9 </p>
<p> Cyclomatic Complexity: </p>
<p> <img width="650" alt="Screen Shot of Radon" src = "https://user-images.githubusercontent.com/70499767/208593342-48856997-bef5-4408-b8f4-5b9bd4371825.png"> </p>
<p> <img width="650" alt="ScreenShot of Radon Two" src="https://user-images.githubusercontent.com/70499767/208593496-03935346-9f8b-4dc1-b7cf-15a66467c40c.png"> </p>
<p></p>
<p>Maintainability Index: </p>
<p> <img width="650" alt="ScreenShot of Radon Three" src="https://user-images.githubusercontent.com/70499767/208593582-13dfae9b-ed6a-48e3-ba84-5ac37f81fa27.png"> </p>




### Contribution List: 
* Calvin: Created burndown chart, reviewed pull requests, added more testing, and added post-refactor radon output.
* Matt:
* Ben: refactored graph code to reduce length of views.py, set up heroku deployment [here](https://colby-athlete-managment-system.herokuapp.com), created oauth.py to handle oauth2 flow
* Milo: Increased test coverage by 11%, configured pytest and radon with custom repository commands, collected code complexity metrics and refactored views and auth.
* Tamsin: scrum master, wrote and posted issues for new milestone, fixed team breakdown table to reflect real data, improved formatting in athlete breakdown table, fixed bug where roles were not being assigned/User table was not being created, cleaned up name variables to standardize capitalization and spacing, cleaned up and linted code, connected dashboard stats table to database so it reflects real changes in data over time, connected coach schedule to Google calendar
* Anton: 

### NEW FEATURE SUMMARY: 
Functional Heroku deployment:
<img width="1411" alt="Screen Shot 2022-12-19 at 5 40 27 PM" src="https://user-images.githubusercontent.com/30237570/208540616-9bc46432-e131-4bbe-bc04-d09092755f1c.png">
Dashboard stats table now reflects real database data:
<img width="1299" alt="Screen Shot 2022-12-19 at 5 41 57 PM" src="https://user-images.githubusercontent.com/30237570/208540837-d5d8b2e5-836c-4ce9-b1ad-cc7da02e0835.png">
Functional & unit tests for new features
Connected Google Drive API to database


### Extensions: 
* Functional ReadMe file to our repository detailing the website.


### References: 
Naser Al Madi

