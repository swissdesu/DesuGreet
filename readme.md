# DesuGreet
DesuGreet is a small discord bot. it assigns a role to new members and welcomes them on the server with a direct message.

# Install
1. `git clone https://github.com/swissdesu/DesuGreet`
2. `pip install ./DesuGreet`
3. create a file with the name .desugreet in your home directory
4. The content of the config file should look like this:

```JSON
{
"token": "your top secret token",
"member-role": "Member-Role-Name",
"entrance-role": "Entrance-Role-Name",
"entrance-channel-id": "channel ID of the entrance channel",
"entrance-message": "Welcome message in entrance channel that tags the joined user with {0.mention}",
"welcome-message": "Welcome message that is sent in the DM on accepting the User. It tags the user with {0.mention} and welcomes to the server with name {1.name}",
"log-channel-id": "channel ID of the log channel"
}
```

# Run
you can run it via the terminal with the command `desugreet`.

# Commands
* To check how long your bot has been running just type `!dginfo` in the chat.

* To delete all messages in the entrance channel, type `!clear-entrance` in the chat.  
The user running this command must have the 'manage_messages' permission.

# Licence
DesuGreet is licensed under GPL2.