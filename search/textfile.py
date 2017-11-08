# Search the given file for the incoming search terms


def searchFile(filename,**kwargs):
    try:
        logfile = None
        filenameprinted = False
        if kwargs['logfile']:
            logfile = open(kwargs['logfile'], 'a')
        with open(str(filename), 'r') as fil:
            searchstring = 'Searching file {0}\n'.format(filename)
            if kwargs['verbose']:
                print('\n'+searchstring)
                if logfile:
                    logfile.write(searchstring+'\n')
                    filenameprinted = True
            linecount = 0
            for i in fil:
                linecount += 1
                for q in str(kwargs['searchphrase']).split(','):
                    if (q != '') and q in i:
                        if not filenameprinted:
                            print('\n' + searchstring)
                            if logfile:
                                logfile.write(searchstring + '\n')
                            fileprinted = True
                        if kwargs['verbose']:
                            verboseline = '\nSearchphrase {0} found at'.format(q)
                            print(verboseline)
                            if logfile:
                                logfile.write(verboseline+'\n')
                        outline = 'Line {0}: {1}\n'.format(linecount, i.strip())
                        print(outline)
                        if logfile:
                                logfile.write(outline+'\n')
    except Exception as e:
        print('\nAn exception has occurred, please review the error and try again!\n\n{0}'.format(e))
    finally:
        try:
            logfile.close()
        except:
            pass