hacer
=====

hacer is a simple command-line-based quiz game for learning Spanish verb
conjugations. It only tests you on stuff you think you ought to know. I
personally add to the list of verbs whenever I encounter a new one on Duolingo.

Usage
-----

Just type

    $ python3 hacer.py

to set up a minimal config, update conjugations from web, and play.

Configuration
-------------

hacer will only quiz you on the stuff you know, or should know. Edit the files
in the `config/` directory to tell hacer what you want to be tested on.
Available options for `persons`, `numbers`, and `tenses` are in the `hacer.py`
source file. The `verbs` file should be able to contain any verb infinitive.
When you start hacer, it will automatically grab conjugations for new verbs
from the web.

Requirements
------------

  - Python 3.3+
  - BeautifulSoup 4

Caveats
-------

  - Python 3 only
  - Virtually no error handling
  - Like me, currently only knows about indicative mood
  - Knows nothing of vosotros verb conjugations (I'm not near Spain)
  - File layout unsuitable for system-wide installation
  - No rhyme or reason to word/conjugation selection during quiz
  - Depends on BeautifulSoup, which is overkill for the simple scraping task
  - You should probably use an international keyboard layout
  - and many more!
