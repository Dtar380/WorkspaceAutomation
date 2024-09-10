# History

### The problem
I was searching for ways to waste less time with all that boring repetitive stuff so I could be more productive and spend more time coding. I started by automating Git tasks with GitHub actions like managing issues and pull requests, and also how to automatically publish my packages when creating a new release tag on GitHub.<br>
But after that I didn't feel like that was enough time saving, because all those tasks weren't actually taking much time, yes they where repetitive and boring, but you don't create a release, or manage issues and pull requests often enough to actually say it's taking a significant part of your time.<br>

### The idea
Thats when it clicked, I can automate the most common and done task of every programmer, opening your working tools to work on a project, a thing that we all do at least once a day, and maybe if you're working on multiple projects you'll need to re open each program used for each project.<br>

### Selecting the language
I decided to make it on python because it's my language of choice for my personal repositories, because it's easy and quick to write on, and I do not want to spend tons of hours in something that is only for fun and Im not going to make a profit with, basically because I have other important stuff that actually needs to get done.<br>
And also because even though python is known as a language that lacks of performance, this app didn't required that, and I tested it against rust which was my other way to go, and for earning 2-3 seconds of time we wouldn't be making a difference (rust was taking under .4 second to execute the most demanding tasks while python was taking 8 times more at most), taking the fact that this app will already be saving minutes on the daily.<br>

### Open sourcing it
The project started as a small personal project, I tested it and used it for some time, until I went onto the [python discord comunity](https://discord.com/invite/python) and commented about my application, and I did a very simple question _"Should I open-source it?"_, I got this answer that now I take as a life lesson _"If you're not planning on charging for the program, and the other option is not doing it, why not?"_, so I got to work and I started this project.<br>

I first took all my personal project and see how could I make that more mantainable (the OG code was 1000 lines of spaghetti code that I was the only capable of reading it, and not always), so I started by thinking about using classes for each feature, some main classes to contain the logic. I also had to take all the libraries from the OG project and see which ones I really needed, because I don't like depending on a library for only using it 3 times on the code if I can make it my self.<br>
And after all of that decision making and structuring I started coding and refactoring everything to meet the demands I made my self about the project.<br>

### Currently
And now after a month since I started we are here, the project already on its first release and working on further adding features I didn't thought of and I actually doing and I found that are actually very interesting of adding and might be helpful to lots of fellow programers.
