# DesuGreet
DesuGreet is a small discord bot. it assigns a role to new members and welcomes them on the server with a direct message.

# Install
1. `git clone https://github.com/AlexFence/DesuGreet`
2. `pip install ./desugreet`
3. create a file with the name .desugreet in your home directory
4. The content of the config file should look like this:
```JSON
{
    "token":"your_super_secret_bot_token",
    "role":"your cool member role",
    "message":"Hi {0.mention}, welcome to {1.name}!"
}
```

# Run
you can run it via the terminal with the command `desugreet`.

To check how long your bot has been running just type !dginfo in the chat.

# Licence
DesuGreet is licensed under GPL2.
