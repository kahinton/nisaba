# Attempts to modify the file line by line given the user selected parameters

import fileinput

def alterFile(filename,**kwargs):
    try:
        logfile = None
        if kwargs['logfile']:
            logfile = open(kwargs['logfile'], 'a')
        alterstring = 'Attempting to alter file {0}\n'.format(filename)
        print('\n'+alterstring)
        if logfile:
            logfile.write(alterstring+'\n')
            
        # Output needs to be stored in a list due to how fileinput takes over the standard output
            
        changeList = []
        linecount = 0
        for line in fileinput.input(filename, inplace=True):
            linecount += 1
            f = line
            for ex in str(kwargs['alter']).split(','):
                split = ex.split('->')
                if split[0] in f:
                    if kwargs['verbose']:
                        verboseline = 'Found term {0}, replacing with {1}'.format(split[0], split[1])
                        changeList.append(verboseline)
                    f = f.replace(split[0], split[1]).replace('\n', '')
                    changeList.append('Line {0}: {1}'.format(linecount, f))
            print(f.strip('\n'))
        
        for outline in changeList:
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