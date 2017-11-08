import click
import os
from alter.altertext import alterFile
from search.textfile import searchFile
from search.jsonfile import jSearchFile

__author__ = "Kyle Hinton"
__version__ = "1.0.0"
__maintainer__ = "Kyle Hinton"
__status__ = "Production"

# Making strings for the help documentation

alter = 'Optional*: Provide Nisaba a list of words or phrases that you would like \
to be replaced. These entries should take the form "old->new". Multiple entries \
should be separated by a comma. If you do not select the alter option, you must \
use the searchphrase option.'

searchphrase = 'Optional*: Provide Nisaba a list of words to search for. Multiple \
entries should be comma separated. If this option is not used, you must use the \
alter option.'

logfile = 'Optional: Provide Nisaba with a path to a file that you would like the \
results of your work logged to.'

filetype = 'Optional: If you would only like Nisaba to search through certain \
types of files, provide a comma separated list of their file extensions using \
this option. Note that the extension should include the "."'

verbose = 'Optional: If you would like some more output about what Nisaba has \
found, simply provide this tag.'

recursive = 'Optional: If you would like Nisaba to search through all of the \
subdirectories of your selected folder, provide this option. Do consider how many \
files this may end up causing Nisaba to search through.'

searchkeys = 'Required: Provide Nisaba the terms that you would like to find in \
a given key. The entries should have the format "key::phrase". Mulitple entries \
should be comma separated.'

outkeys = 'Optional: Provide Nisaba with a list of the keys that you would like \
to be output. Mulitple key entries should be comma separated. Note that if no keys \
are provided, Nisaba will default to providing the entire string of JSON.'


@click.group()
@click.version_option(version = __version__)
def init():
    """Nisaba is a multi-functional work tool for searching through and altering
    text in files. The results of operations can optionally be stored in log files
    to keep track of you work. Use the help command on the functions of Nisaba to
    see further explanations of their features."""
    pass


@init.command()
@click.argument('rootfolder')
@click.option('-a', '--alter', default = None, help = alter)
@click.option('-s', '--searchphrase', default = None, help = searchphrase)
@click.option('-l', '--logfile', default = None, help = logfile)
@click.option('-f', '--filetype', default = '.*', help = filetype)
@click.option('-v', '--verbose', is_flag = True, help = verbose)
@click.option('-r', '--recursive', is_flag = True, help = recursive)
def folder(**kwargs):
    """By supplying a path to the folder that you would like to search, this will
    set Nisaba to work finding the requested entries in the text, or altering your
    files where needed. Note that if you want to search through all of the 
    sub-directories of your folder, you just need to add the recursive option."""
    try:
        if not kwargs['recursive']:
            files = os.listdir(kwargs['rootfolder'])
            foundfiles = 0
            for q in files:
                if kwargs['filetype'] == '.*' and '.' in q[-4:]:
                    filepath = os.path.join(kwargs['rootfolder'], q)
                    foundfiles += 1
                    if kwargs['alter'] is None and kwargs['searchphrase']:
                        searchFile(filepath, **kwargs)
                    elif kwargs['alter'] and kwargs['searchphrase'] is None:
                        alterFile(filepath, **kwargs)
                    else:
                        print('\nPlease specify either alter or searchphrases')
                    
                elif '.{0}'.format(q.split('.')[-1]) in str(kwargs['filetype']).split(','):
                    filepath = os.path.join(kwargs['rootfolder'], q)
                    foundfiles += 1
                    if kwargs['alter'] is None and kwargs['searchphrase']:
                        searchFile(filepath, **kwargs)
                    elif kwargs['alter'] and kwargs['searchphrase'] is None:
                        alterFile(filepath, **kwargs)
                    else:
                        print('\nPlease specify either alter or searchphrases')
                        
            if foundfiles == 0:
                print('\nNo files found with the file extension(s) {0}'.format(str(kwargs['filetype'])))
            else:
                if kwargs['verbose']:
                    print('\n{0} files searched'.format(foundfiles))

        if kwargs['recursive']:
            foundfiles = 0
            for root, dirs, files in os.walk(kwargs['rootfolder'], topdown=False):
                for name in files:
                    if kwargs['filetype'] == '.*' and '.' in name[-4:]:
                        filepath = os.path.join(root, name)
                        foundfiles += 1
                        if kwargs['alter'] is None and kwargs['searchphrase'] is not None:
                            searchFile(filepath, **kwargs)
                        elif kwargs['alter'] is not None and kwargs['searchphrase'] is None:
                            alterFile(filepath, **kwargs)
                        else:
                            print('\nPlease specify either alter or searchphrases')
                            
                    elif '.{0}'.format(name.split('.')[-1]) in str(kwargs['filetype']).split(','):
                        filepath = os.path.join(root, name)
                        foundfiles += 1
                        if kwargs['alter'] is None and kwargs['searchphrase'] is not None:
                            searchFile(filepath, **kwargs)
                        elif kwargs['alter'] is not None and kwargs['searchphrase'] is None:
                            alterFile(filepath, **kwargs)
                        else:
                            print('\nPlease specify either alter or searchphrases')
                            
            if foundfiles == 0:
                print('\nNo files found with the file extension(s) {0}'.format(str(kwargs['filetype'])))

            else:
                if kwargs['verbose']:
                    print('\n{0} files searched'.format(foundfiles))
    except Exception as e:
        print('\nNisaba encountered the following error: {0}'.format(e))


@init.command()
@click.argument('file')
@click.option('-a', '--alter', default = None, help = alter)
@click.option('-s', '--searchphrase', default = None, help = searchphrase)
@click.option('-l', '--logfile', default = None, help = logfile)
@click.option('-v', '--verbose', is_flag = True, help = verbose)
def file(**kwargs):
    """If you need Nisaba to search through a single file, you should use this option.
    Simply provide the filepath, and your required options, and Nisaba will do the rest!"""
    if kwargs['alter'] is None and kwargs['searchphrase']:
        searchFile(kwargs['file'], **kwargs)

    elif kwargs['alter'] and kwargs['searchphrase'] is None:
        alterFile(kwargs['file'], **kwargs)

    else:
        print('\nPlease specify either alter or searchphrases')
    print('\nFile search is finished')


@init.command()
@click.argument('file')
@click.option('-s', '--searchkeys', default = None, help = searchkeys)
@click.option('-o', '--outkeys', default = None, help = outkeys)
@click.option('-l', '--logfile', default = None, help = logfile)
@click.option('-v', '--verbose', is_flag = True, help = verbose)
def jfile(**kwargs):
    """If your file stores lines in JSON format, Nisaba can do some special search
    functions. Using the options available to this function, you should be able to
    return very specific information from your file."""
    
    if kwargs['searchkeys']:
        jSearchFile(kwargs['file'], **kwargs)

    else:
        print('\nPlease specify desired searchkeys')
    print('\nFile search is finished')
    
    
@init.command()
@click.argument('rootfolder')
@click.option('-s', '--searchkeys', default = None, help = searchkeys)
@click.option('-o', '--outkeys', default = None, help = outkeys)
@click.option('-l', '--logfile', default = None, help = logfile)
@click.option('-f', '--filetype', default = '.*', help = filetype)
@click.option('-v', '--verbose', is_flag = True, help = verbose)
@click.option('-r', '--recursive', is_flag = True, help = recursive)
def jfolder(**kwargs):
    """If you have folders containing multiple files that have lines in JSON format,
    this function will sort thorugh them in short order. If you need to search all
    subdirectories, simply use the recursive optoin."""
    try:
        if kwargs['recursive'] is False:
            files = os.listdir(kwargs['rootfolder'])
            foundfiles = 0
            for q in files:
                if kwargs['filetype'] == '.*' and '.' in q[-4:]:
                    filepath = os.path.join(kwargs['rootfolder'], q)
                    foundfiles += 1
                    if kwargs['searchkeys']:
                        jSearchFile(filepath, **kwargs)
                    else:
                        print('\nPlease specify desired searchkeys')
                    
                elif '.{0}'.format(q.split('.')[-1]) in str(kwargs['filetype']).split(','):
                    filepath = os.path.join(kwargs['rootfolder'], q)
                    foundfiles += 1
                    if kwargs['searchkeys']:
                        jSearchFile(filepath, **kwargs)
                    else:
                        print('\nPlease specify desired searchkeys')
                        
            if foundfiles == 0:
                print('\nNo files found with the file extension(s) {0}'.format(str(kwargs['filetype'])))
            else:
                if kwargs['verbose']:
                    print('\n{0} files searched'.format(foundfiles))
        if kwargs['recursive']:
            foundfiles = 0
            for root, dirs, files in os.walk(kwargs['rootfolder'], topdown=False):
                for name in files:
                    if kwargs['filetype'] == '.*' and '.' in name[-4:]:
                        filepath = os.path.join(root, name)
                        foundfiles += 1
                        if kwargs['searchkeys']:
                            jSearchFile(filepath, **kwargs)
                        else:
                            print('\nPlease specify desired searchkeys')
                            
                    elif '.{0}'.format(name.split('.')[-1]) in str(kwargs['filetype']).split(','):
                        filepath = os.path.join(root, name)
                        foundfiles += 1
                        if kwargs['searchkeys']:
                            jSearchFile(filepath,**kwargs)
                        else:
                            print('\nPlease specify desired searchkeys')
                            
            if foundfiles == 0:
                print('\nNo files found with the file extension(s) {0}'.format(str(kwargs['filetype'])))
            else:
                if kwargs['verbose']:
                    print('\n{0} files searched'.format(foundfiles))
    except Exception as e:
        print('\nCodeCrawler encountered the following error: {0}'.format(e))
            
if __name__ == '__main__':
    init()
