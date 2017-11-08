import json


def jSearchFile(filename,**kwargs):
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
                
                try:
                    decoded = json.loads(i)
                except:
                    print('Line {0} failed to parse as json'.format(linecount))
                    
                for q in str(kwargs['searchkeys']).split(','):
                    pair = q.split('::')
                    if pair[1] in decoded[pair[0]]:
                        if not filenameprinted:
                            print('\n' + searchstring)
                            if logfile:
                                logfile.write(searchstring + '\n')
                        if kwargs['verbose']:
                            verboseline = '\nSearchkey pair {0}:{1} found at'.format(pair[0],pair[1])
                            print(verboseline)
                            if logfile:
                                logfile.write(verboseline+'\n')
                        outline = 'Line {0}: '.format(linecount)
                        if kwargs['outkeys']:
                            for u in kwargs['outkeys'].split(','):
                                outline += '{0}:{1} '.format(u, decoded[u])
                        else:
                            outline += i
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