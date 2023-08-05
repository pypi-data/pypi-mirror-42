from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from builtins import super
from future import standard_library
standard_library.install_aliases()
from builtins import object
from re import sub

from .args import HELP, LIST_INDEX, DATADIR, INIT_REPOSITORY, RETRIEVE, TEMPDIR, INGEST, INDEX, SUBSCRIBE, \
    AVAILABILITYURL, DATASELECTURL, DOWNLOAD, LIST_RETRIEVE, mm, ALL, MSEEDINDEXCMD, Arguments, MDFORMAT, FILE, START, \
    STATUS, STOP, LIST_SUBSCRIBE, UNSUBSCRIBE, TRIGGER, DAEMON, LIST_SUMMARY, SUMMARY, DEFAULT_FILE, INIT_REPO, INIT, \
    RETRIEVE_METADATA

"""
The 'rover help' command.
"""


BACKGROUND = 'background'
USAGE = 'usage'
LOWLEVEL = 'low-level'


def welcome(config):
    return '''
                      Welcome to ROVER!

For more information on ROVER commands:
  
rover %s %s

  Displays information on the most common commands to immediately 
  download and ingest data.
    
rover %s %s

  Covers Rover's advanced mode, where it runs in the background, 
  continuously checking subscriptions and downloading data when 
  needed.
    
rover %s %s

  Lists lower-level commands that are less likely to be used.
  
Individual commands also have help.  See "rover %s %s".
    
For more information on configuration parameters, which can be 
provided via a file or using command line flags:

  rover -h

    Displays the command line parameters.
  
  %s

    Contains the defaults for these parameters and can be edited 
    to change the default behaviour.
    
To display this screen again, type "rover" or "rover help".

''' % (HELP, USAGE,
       HELP, BACKGROUND,
       HELP, LOWLEVEL,
       HELP, HELP,
       DEFAULT_FILE)


def usage(config):
    return '''
                    Common Rover Commands
                    
rover %s [directory]

  Initialize the given directory (or the current directory)
  as the repository.  This will create a configuration file
  (by default %s) as well as directories for logs and data.
  
  The aliases `rover %s` and `rover %s` also exist.

rover %s (file | sta=... [start [end]] | N_S_L_C [start [end]])

  Compare the local index with the data available remotely 
  (config parameter %s), then download (config parameter 
  %s) and ingest the missing files.  Use %s (below) to
  see what data would be downloaded (without doing the work).
  
rover %s (file | sta=... [start [end]] | N_S_L_C [start [end]])

  Compare the local index with the data available remotely 
  (config parameter %s), then display the difference.  
  Note that the summary is printed to stdout, while logging is 
  to stderr.

rover %s ...

  List index entries for the repository (config parameter 
  %s) that match the given constraints.  For more information, 
  run "rover %s" (with no arguments).

rover %s ...

  List summary entries for the repository (config parameter 
  %s) that match the given constraints.  This is faster than
  `rover %s` but gives less detail.  For more information, 
  run "rover %s" (with no arguments).

''' % (INIT_REPOSITORY, DEFAULT_FILE, INIT, INIT_REPO,
       RETRIEVE, AVAILABILITYURL, DATASELECTURL, LIST_RETRIEVE,
       LIST_RETRIEVE, AVAILABILITYURL,
       LIST_INDEX, DATADIR, LIST_INDEX,
       LIST_SUMMARY, DATADIR, LIST_INDEX, LIST_SUMMARY)


def background(config):
    return '''
                   Advanced Rover Commands
    
rover %s

  Start the background process that regularly downloads subscriptions.
  
rover %s

rover %s

  Display the status of, and stop, the background process.
                   
rover %s (file | sta=... [start [end]] | N_S_L_C [start [end]])

  Subscribe to retrieve updates whenever they become available.
  This has the same syntax as `rover %s`, but runs regularly in
  the background.
  
rover %s

rover %s N

  The first form lists the subscriptions.  The second shows
  which data will be downloaded for that subscription (similar to
  `rover %s`).
  
rover %s N

  Ask the background daemon to process the given subscription
  immediately, rather than waiting for the next update.
  
rover %s N

  Delete the subscription (the data remain in the repository, 
  but no more downloads will be made) 
  
''' % (START, STATUS, STOP,
       SUBSCRIBE, RETRIEVE,
       LIST_SUBSCRIBE, LIST_SUBSCRIBE, LIST_RETRIEVE,
       TRIGGER, UNSUBSCRIBE)


def low_level(config):
    return '''
                   Low-Level Rover Commands
                   
The following commands are used internally, but are usually not
useful from the command line:

rover %s url

  Download data from the given URL to the temporary store
  (config parameter %s).  When downloaded, ingest into the
  repository (config parameter %s) and delete.  Called
  by %s and the %s when needed.

rover %s (file|dir) ...

  Add the specified files to the repository (config
  parameter %s) and update the database index 
  Called by %s when needed.
  
rover %s [(file|dir) ...]

  Scan files and update the database index using the mseedindex 
  command (config parameter %s). Called by %s when needed.
  
  If no arguments are given then files in the repository
  (config parameter %s) that have been modified since the 
  repository was last indexed are processed.  The config 
  parameter %s can be used (eg %s on the command line) to force 
  processing of all files in the repository.
  
rover %s

  Re-generate the summary table used by `rover %s`.

rover %s

Download missing metadata from the fdsnws-station web service and save to the
data archive. This feature is only supported for the ASDF output format.
      
''' % (DOWNLOAD, TEMPDIR, DATADIR, SUBSCRIBE, DAEMON,
       INGEST, DATADIR, RETRIEVE,
       INDEX, MSEEDINDEXCMD, INGEST, DATADIR, ALL, mm(ALL),
       SUMMARY, LIST_SUMMARY, RETRIEVE_METADATA)


GENERAL = {
    USAGE: (usage, 'General interactive use'),
    BACKGROUND: (background, 'Advanced use with rover in the background'),
    LOWLEVEL: (low_level, 'Rarely used, low-level commands')
}


class HelpFormatter(object):
    """
    Either print markdown verbatim. or strip markdown and re-justify for 80 columns.
    """

    def __init__(self, md_format):
        self._md_format = md_format

    def print(self, text):
        arguments = Arguments()
        first_param = True
        for line in self.__paras(text):
            if line.startswith('@'):
                if first_param:
                    arguments.print_docs_header()
                    first_param = False
                if self._md_format:
                    arguments.print_docs_row_md(line[1:])
                else:
                    arguments.print_docs_row_text(line[1:])
            elif self._md_format:
                print(self.__escape(line))
            elif line.startswith('#'):
                print(line.lstrip(' #'))
            else:
                for short in self.__splitlines(line):
                    print(short)

    def __escape(self, text):
        text = sub(r'\\', '\\\\', text)
        # text = sub(r'`', '\\`', text)
        return text

    def __paras(self, text):
        lines = text.splitlines()
        i = 1
        while i < len(lines):
            if lines[i].strip() and lines[i-1].strip() and not lines[i].startswith('@') and not lines[i-1].endswith('\\'):
                lines[i-1] = lines[i-1].rstrip() + ' ' + lines[i].strip()
                lines[i:] = lines[i+1:]
            else:
                i += 1
        return lines

    def __slurp(self, line):
        word = ''
        space = ''
        while line and not line[0] == ' ':
            word += line[0]
            line = line[1:]
        while line and line[0] == ' ':
            space += line[0]
            line = line[1:]
        return word, space, line

    def __splitlines(self, line):
        indentation = ''
        while line and line.startswith(' '):
            indentation += line[0]
            line = line[1:]
        if not line:
            yield ''
            return
        while line:
            short, space = indentation, ''
            line = line.lstrip()
            while line:
                word, next_space, next_line = self.__slurp(line)
                if short.strip() and len(short + space + word) > 78:
                    yield short
                    short, space = indentation, ''
                else:
                    short = short + space + word
                    space, line = next_space, next_line
            if short:
                yield short


class Helper(HelpFormatter):

    def __init__(self, config):
        super().__init__(config.arg(MDFORMAT))
        self._config = config

    def run(self, args):
        from rover import COMMANDS   # avoid import loop
        if not args:
            self.print(welcome(self._config))
            return
        elif len(args) == 1:
            command = args[0].lower()
            if command == 'help':
                self._help()
                return
            if command in COMMANDS:
                self.print(COMMANDS[command][0].__doc__)
                return
            elif command in GENERAL:
                self.print(GENERAL[command][0](self._config))
                return
        raise Exception('Help is available for: %s, %s, %s, and individual commands (or simply "rover help")' % (USAGE, BACKGROUND, LOWLEVEL))

    def _help(self):
        from rover import COMMANDS   # avoid import loop
        self.print('''
### Help

Gives help on the various commands.
        
Help is available for the following commands:
        ''')
        for command in sorted(COMMANDS.keys()):
            print('%19s: %s' % (command, COMMANDS[command][1]))
        print('''
Help is also available for the following general topics: 
''')
        for command in GENERAL.keys():
            print('%19s: %s' % (command, GENERAL[command][1]))
        print('''
For example:

    rover help retrieve
''')
