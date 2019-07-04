![](https://cdn.discordapp.com/attachments/594172292594925568/594172367505457152/introduction2.png) 

Hello there. I am so eager to play with you. Before you request me to join your server, I do also have a little request for you to keep. I require an **`Administrative`** priviledge on your server because that helps me to run correctly.<br>
*And if you like me, don't forget to star this repository.*<br>
***So what are you waiting for? Come, let's join the adventure!***

[![](https://cdn.discordapp.com/attachments/594172292594925568/594196409385746514/invite_dschackweek_longversion_512.png)](https://discordapp.com/api/oauth2/authorize?client_id=554689083289632781&permissions=8&scope=bot)
[![](https://cdn.discordapp.com/attachments/594172292594925568/594458570632855563/invite_dschackweek_jumpinforsupp_330.png)](https://discord.gg/qPnmfh4)



# Table of Contents

- [Setup](#Setup)
- [Usage Policy](#Usage-Policy)
- [Prefix & Commands](#Prefix--Commands)
    - [Game](#Game-)
    - [9gag](#9gag-)
    - [COC](#COC-)
    - [Jokes](#Jokes-)
    - [Translator](#Translator-)
- [Contributors](#Contributors)
 

# Setup
*Honestly my setup can be a bit difficult. But still if you would like to run me on your local server then strictly follow the steps.*

1. Get a discord bot token. Instructions can be found [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token).

2. Get a COC token.

    1. Make an account [here](https://developer.clashofclans.com) and login.
    2. Then go [here](https://developer.clashofclans.com/#/account) and create new key.
    3. Give a key name, description and your public IP address for which you want to generate a token.

3. Gather your mysql server's username, password. This will be used as a database for translations.

4. Clone this repository.

5. Install all your required libraries using `pip install -r requirements.txt`.

6. You need to setup the environment variables as follows. If you don't know how to setup environment variables, then check [here](https://www.schrodinger.com/kb/1842).

    1. TOKEN=Put your bot token here
    2. COC=Put your clash of clans token here. 
    3. user=Put your mysql server's username here.
    4. password=Put your mysql server's password here.
    5. url=Put your mysql server url here.
    
7. Congrats! Now you can run `tsuby.py` and this is how you can host me on your local server.

<br>

# Usage Policy
*First of all thanks to all for visiting my repository. If you wish to use my existing codes, please don't forget to credit my team. I won't mind you use all my codes, as I am open source for a reason, as long as you don't blindly copy it or refraining from crediting my team. Give credit where it is due.*

<br>

# Prefix & Commands

### Prefix
*My prefix is case-insensitive.*

|Option|Default|Example|
|------|-------|-----------|
| Prefix|`t-`|`t-help`| 
 
<br>

### Utility Commands
*These are some of my utility commands.*

|Option|Commands|Description|
|------|-------|-----------|
|**feedback**|`t-feedback <msg>`|Send feedback to my owner.|
|**info**|`t-help`| Lists some general info about me.|
|**nitromojis**|`t-nitromojis` _then_ `t-ne <nitromojiname>` _to use_ | Lists all the nitromojis and let you use nitromojis from the list.|
|**ping**|`t-ping`|Ping me!|
|**react**|`t-react <emoji>`_or_`<nitromojiname>` | Tsuby will react to the last message of any user.|

<br>

### Game <br>
*I do have some games to kill your time. Don't forget to check it out. ;)*

|Option|Command|Description|
|------|-------|-----------|
|**game help**|`t-game help`| All the available games and their related commands.|

#### Game related commands:

|Option|Commands|Description|
|------|-------|-----------|
|**tictactoe**|`t-game tictactoe <@user>`| Play tictactoe with your friend.|
|**guess**|`t-game guess` | Play a person-guessing game with me.|

<br>

### 9gag <br>
*Aaaha! With the new invention of **`infinite-post`** by my owner, these commands are one of the must-try ones.*<br>
*Nope, no, if you think that this would spam, then you have probably misunderstood the `infinite-post`.*

|Option|Command|Description|
|------|-------|-----------|
|**9gag help**|`t-9gag help`| All the available memes related commands.|

#### 9gag related commands:

|Option|Commands|Description|
|------|-------|-----------|
|**sections**|`t-9gag sections`| Get the list of 9gag categories.|
||`t-9gag <section name>(optional)`| Get random post from 9gag.com.|
|**popular**|`t-9gag <popular>(optional) <sections>(optional)`| Get random posts from 9gag.com. <br> The <_popular_> includes "_Trending_" and "_Fresh_".|
|**search**|`t-9gag search <query>`| Get your search result from 9gag.com.|

<br>

### COC <br>
*My owner and supporter were really addictive to this game. :p <br>
Well who doesn't want to get stats of 'player' and 'clan' right from the discord?* ^^

|Option|Command|Description|
|------|-------|-----------|
|**coc help**|`t-coc help`|  All the Clash of Clans related commands.|

#### COC related commands:

|Option|Commands|Description|
|------|-------|-----------|
|**clan**|`t-coc clan <clan_tag>`| Fetch information about the given clan.|
|**player**|`t-coc player <player tag>`| Fetch information about the given player.|

<br>

### Jokes <br>
*Wife: “Windows frozen.” <br>
Husband: “Pour some warm water over them.” <br>
Wife: “Computer completely screwed up now.”* <br>

*Hahaha...sometimes, I can be really funny as well.* ;)

|Option|Command|Description|
|------|-------|-----------|
|**jokes help**|`t-jokes help`|All the available jokes related commands.|

#### Jokes related commands:

|Option|Commands|Description|
|------|-------|-----------|
|**category**|`t-jokes category`| Get the list of jokes categories
||`t-jokes <category>(optional)`| Get some random jokes.

<br>

### Translator <br>
*Do you ever need any help with some random visitors in your server who don't speak your language but you want him to take part in the conversation?*
*Invite me and I can be your translator.* ;)

|Option|Command|Description|
|------|-------|-----------|
|**tr help**|`t-tr help`|All the translation related commands.|

#### Translator related commands:

|Option|Commands|Admin Required| Description|
|------|-------|--------|-----------|
|**codes**|`t-tr codes`| No|Get the list of language codes.|
|**fr**|`t-tr fr <destination><source>[<user><user>...<user>]`|Yes| Enables auto translation of the messages to the 'dest.' language from the 'src' language of all the mentioned 'user'|
|**ignore** | `t-tr ignore [<word> <word> ... <word>]`|Yes|Ignores auto-translating the message when started with the given words. Usually 'word' contain other bot's prefixes. <br> **Warning:** *Once the words is added, it cannot be removed.*|
|**leave**| `t-leave` | Yes | Removes all the user's settings of that guild and leaves.|
|**remove**|`t-tr remove [<user> <user> ... <user>]`|Yes|Disable auto translation of all the mentioned 'user'.|
|**to**| `t-tr to <dest.> <src> <message>`|No| Translate the message to the 'dest.' language from the 'src' language.|

##### Translator sub commands:

|Option|Command|Description|
|------|-------|-----------|
|**auto on/off**|`t-tr auto on <dest.><src>`|Enable server-wide auto-translation of your message to the 'dest.' language from the 'src' language.|
||`t-tr auto off` | Disable your server-wide auto-translation.|
|**ch on/off**| `t-tr ch on <dest.><src>`|  Enable channel-wide auto-translation of your message to the 'dest.' language from the 'src' language.|
||`t-tr ch off`| Disable your channel-wide auto-translation|

# Contributors
*These are the discord people without whom I could not have born.* :p
- `Tsubasa#7917 (my owner)`
- `Linus#0002 (my supporter)`

I would also like to thank `Zaxs Souven#4045` for giving me such a wonderful name.
