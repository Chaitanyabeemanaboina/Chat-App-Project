# Chat-App-Project
Chat-App-Project
In this project, we achieved REAL-TIME COMMUNICATION using WEBSOCKETS implemented by Django Channels.

How to Use It
1. Signup and Login
    - Sign up and log in as you do on all websites.
2. Main Page
After logging in, you will arrive at a page containing a form with the following options:
   - Create Group
        You can create a group with any name.
   - Private/Public
        Specify whether you want to create a private or public group.
            Private group: Doesn't allow access unless you accept the request sent by others to join the group.
   - Search Group
        Search for existing groups you want to join.
            If the group is private, a message will pop up saying, "Your request is sent to the admin. Wait until they accept it."
            If you created a private group and another user sends a request, that request will be displayed on the page with an "Accept Request" button. Clicking this button grants the user access to the group.
   - Notifications
        Check for any new messages that you haven't read.
   - Logout
        Use this to log out of the application.
3. Chat Page
    - After clicking submit, you will be navigated to the main chat page.
        Online/Offline Status
            This feature is enabled only in groups containing 2 users. One user can check if the other user is online or offline.
    - Send Button
        Sends the message you entered in the input field.
    - Choose Image
        Select an image to send to the user by clicking the "Send Image" button.
    - Home Button
        Clicking this button disconnects you from the chat and navigates you to the home page.
