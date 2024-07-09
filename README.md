# Chat-App-Project
- In this project,we achieved REAL-TIME COMMUNICATION due to the usage of WEBSOCKETS which are implemented by Django Channels .
- What all does this project provide to a user:
  1. User can create a group specifying whether its PRIVATE or PUBLIC,
     if its PRIVATE only the user allowed by the admin will have access to the group,
     if its PUBLIC any one who wants to join can have access to the group.
  2. Users are allowed to SHARE IMAGES ,and other FILES with the members of the group.
  3. Notifications - the user will be notified if there are any unchecked messages,he is updated it accordingly.
  4. FORGET PASSWORD - if any user forgets his/her password he/she will be directed to a path where he should give his username, if it matches any username in database he will be allowed to set his new password which will be updated in the django User model (Django makes sure that all the usernames are unique which allows the above strategy to work) 
  5. Online/Offline - this feature is enabled only in groups containing 2 users,
     one user can check if the other user is online or offline 