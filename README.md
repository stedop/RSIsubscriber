# Notes

There are a few ways already where I can abstract out some things, I am looking forward to a second pass once
it's up and running

*TODO*    This could potentially be turned into a an app class which acts as a wrapper
        for all uses of the bot.  Essentially each class is a service which implements
        an interface, allowing for the extension.  This is much more SOLID

        We can also add actions via an api catcher, This would allow for routing which
        can then be linked to buttons on a subreddit, in theory you could build some
        very interesting mod tools.

        One could setup a website which allows any subreddit to create a username and login
        amd allow the app to access the currently logged in reddit account (the bot account)
        which automatically sets up the bot to that account and  will let you generate the
        code for buttons.  You could even build a little admin to allow them to setup
        catches and actions and even a interface that allows you to add your own extension
        from github

        Error handling can be done by overridden exceptions using sys.excepthook
        Logging can be done using the setHandler method
        Watch this space!!!