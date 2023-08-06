from __future__ import print_function

# For compatibility with old python
try:
    from builtins import input, range
    import configparser
except ImportError:
    from __builtin__ import raw_input, range
    import ConfigParser as configparser
import getpass
import sys
import cx_Oracle
import os
import re

# raw_input only exists in python 2. This will take care of it
try:
    input = raw_input
except NameError:
    pass


configcomment = """#
# Easyaccess default parameters
#
# database        : Default is dessci, change to desoper, destest, desdr and others
#                   Make sure the db-"database" section is in the .desservices.ini
# editor          : Default editor to open from inside easyaccess if $EDITOR is not set
# prefetch        : Prefetch number of rows to get from oracle (not the number of total rows)
#                   This determine the number of trips to the DB to get all results from query
#                   (default: 30000)
# histcache       : The number of line in the history cache (when possible)
# timeout         : The time in seconds before closing a connection for a query to print on screen
#                   If the results are redirected to a file there is not a timeout (default 20 min)
# nullvalue       : The value used to replace null or empty entries when printing into a file
# outfile_max_mb  : Max size of each fits file in MB (default 1GB)
# compression     : Toggles compression on output files (default no)
# autocommit      : Auto commit changes in DB (default yes)
# trim_whitespace : Trim whitespace from strings when uploading data to the DB (default yes)
# desdm_coldefs   : Use DESDM DB compatible data types when uploading data (default yes)

# Display default parameters
#
# color_terminal  : Display colors in terminal (default yes)
# loading_bar     : Display a loading bar when querying the DB (default yes)
# max_rows        : Max number of rows to display on the screen.
#                   Doesn't apply to output files (default 2500)
# width           : Width of the output format on the screen (default 1000)
# max_columns     : Max number of columns to display on the screen.
#                   Doesn't apply to output files (default 50)
# max_colwidth    : Max number of characters per column at display.
#                   Doesn't apply to output files (def. 500)
"""

descomment = """#
# DES services configuration
# Please modify the passwords accordingly
#
"""


def get_config(configfile):
    """
    Loads config file or create one if not
    Returns a configParser object
    """
    config = configparser.ConfigParser()
    configwrite = False
    check = config.read(configfile)
    if check == []:
        configwrite = True
        print('\nCreating a configuration file... at %s\n' % configfile)
#
# easyaccess section
#
    if not config.has_section('easyaccess'):
        configwrite = True
        config.add_section('easyaccess')
    if not config.has_option('easyaccess', 'database'):
        configwrite = True
        config.set('easyaccess', 'database', 'dessci')
    if not config.has_option('easyaccess', 'editor'):
        configwrite = True
        config.set('easyaccess', 'editor', 'nano')
    if not config.has_option('easyaccess', 'prefetch'):
        configwrite = True
        config.set('easyaccess', 'prefetch', '30000')
    if not config.has_option('easyaccess', 'histcache'):
        configwrite = True
        config.set('easyaccess', 'histcache', '5000')
    if not config.has_option('easyaccess', 'timeout'):
        configwrite = True
        config.set('easyaccess', 'timeout', '1200')
    if not config.has_option('easyaccess', 'nullvalue'):
        configwrite = True
        config.set('easyaccess', 'nullvalue', '-9999')
    if not config.has_option('easyaccess', 'outfile_max_mb'):
        configwrite = True
        config.set('easyaccess', 'outfile_max_mb', '1000')
    if not config.has_option('easyaccess', 'autocommit'):
        configwrite = True
        config.set('easyaccess', 'autocommit', 'yes')
    if not config.has_option('easyaccess', 'compression'):
        configwrite = True
        config.set('easyaccess', 'compression', 'no')
    if not config.has_option('easyaccess', 'trim_whitespace'):
        configwrite = True
        config.set('easyaccess', 'trim_whitespace', 'yes')
    if not config.has_option('easyaccess', 'desdm_coldefs'):
        configwrite = True
        config.set('easyaccess', 'desdm_coldefs', 'yes')
#
# display section
#
    if not config.has_section('display'):
        configwrite = True
        config.add_section('display')
    if not config.has_option('display', 'color_terminal'):
        configwrite = True
        config.set('display', 'color_terminal', 'yes')
    if not config.has_option('display', 'loading_bar'):
        configwrite = True
        config.set('display', 'loading_bar', 'yes')
    if not config.has_option('display', 'max_rows'):
        configwrite = True
        config.set('display', 'max_rows', '2500')
    if not config.has_option('display', 'width'):
        configwrite = True
        config.set('display', 'width', '1000')
    if not config.has_option('display', 'max_columns'):
        configwrite = True
        config.set('display', 'max_columns', '50')
    if not config.has_option('display', 'max_colwidth'):
        configwrite = True
        config.set('display', 'max_colwidth', '500')

    check = True
    if configwrite:
        check = write_config(configfile, config)
        config.read(configfile)
    if check:
        return config


def write_config(configfile, config_ob):
    """
    Writes configuration file
    """
    try:
        F = open(configfile, 'w')
        F.write(configcomment + '\n')
        config_ob.write(F)
        F.flush()
        F.close()
        return True
    except:
        print("Problems writing the configuration  file %s" % configfile)
        return False


def get_desconfig(desfile, db, verbose=True, user=None, pw1=None):
    """
    Loads des config file or create one if it does not exist.
    """
    server_desdm = 'desdb.ncsa.illinois.edu'
    server_public = 'desdb-dr.ncsa.illinois.edu'
    port_n = '1521'

    if not db[:3] == 'db-':
        db = 'db-' + db

    config = configparser.ConfigParser()
    configwrite = False
    check = config.read(desfile)
    if check == []:
        configwrite = True
        if verbose:
            print('\nError in DES_SERVICES config file, creating a new one...')
        if verbose:
            print('File might not exists or is not configured correctly')
        if verbose:
            print()

    databases = ['db-dessci', 'db-desdr', 'db-destest', 'db-desoper']

    if db not in databases and not config.has_section(db):
        msg = '\nDatabase entered is not in %s '%databases
        msg += 'or in DES_SERVICE file, continue anyway? [y]/n\n'
        check_db = input(msg)
        if check_db.lower() in ('n', 'no'):
            sys.exit(0)

    # Add the default databases
    if not config.has_section(db):
        if verbose:
            print('\nAdding section %s to DES_SERVICES file\n' % db)
        configwrite = True
        if db == 'db-dessci':
            kwargs = {'host': server_desdm, 'port': port_n, 'service_name': 'dessci'}
        elif db == 'db-desdr':
            kwargs = {'host': server_public, 'port': port_n, 'service_name': 'desdr'}
        elif db == 'db-destest':
            kwargs = {'host': server_desdm, 'port': port_n, 'service_name': 'destest'}
        elif db == 'db-desoper':
            kwargs = {'host': server_desdm, 'port': port_n, 'service_name': 'desoper'}
        else:
            kwargs = {'host': server_desdm, 'port': port_n, 'service_name': db[3:]}
        dsn = cx_Oracle.makedsn(**kwargs)
        good = False
        if user is None:
            for i in range(3):
                try:
                    user = input('Enter username : ')
                    pw1 = getpass.getpass(prompt='Enter password : ')
                    ctemp = cx_Oracle.connect(user, pw1, dsn=dsn)
                    good = True
                    break
                except:
                    (type, value, traceback) = sys.exc_info()
                    print()
                    if value.args[0].code == 28001:
                        print("ORA-28001: the password has expired or cannot be the default one")
                        print("Need to create a new password\n")
                        password = pw1
                        pw1 = getpass.getpass(prompt='Enter new password:')
                        if re.search('\W', pw1):
                            print("\nPassword contains whitespace, not set\n")
                            sys.exit(0)
                        if not pw1:
                            print("\nPassword cannot be blank\n")
                            sys.exit(0)
                        pw2 = getpass.getpass(prompt='Re-Enter new password:')
                        if pw1 != pw2:
                            print("Passwords don't match, not set\n")
                            sys.exit(0)
                        try:
                            ctemp = cx_Oracle.connect(user, password, dsn=dsn, newpassword=pw1)
                            good = True
                            break
                        except:
                            print('\n Check your credentials and/or database access\n')
                            sys.exit(0)
                    print(value)
                    if value.args[0].code == 1017:
                        pass
                    if value.args[0].code == 12514:
                        print("Check that database '%s' exists\n"%db)
                        sys.exit(0)
                    else:
                        sys.exit(0)
            if good:
                ctemp.close()
            else:
                if verbose:
                    print('\n Check your credentials and/or database access\n')
                sys.exit(0)
        config.add_section(db)

    if not config.has_option(db, 'user'):
        configwrite = True
        config.set(db, 'user', user)
    if not config.has_option(db, 'passwd'):
        configwrite = True
        config.set(db, 'passwd', pw1)
    if db == 'db-dessci':
        if not config.has_option(db, 'name'):
            configwrite = True
            config.set(db, 'name', 'dessci')
            if not config.has_option(db, 'server'):
                configwrite = True
                config.set(db, 'server', server_desdm)
    elif db == 'db-desoper':
        if not config.has_option(db, 'name'):
            configwrite = True
            config.set(db, 'name', 'desoper')
            if not config.has_option(db, 'server'):
                configwrite = True
                config.set(db, 'server', server_desdm)
    elif db == 'db-desdr':
        if not config.has_option(db, 'name'):
            configwrite = True
            config.set(db, 'name', 'desdr')
            if not config.has_option(db, 'server'):
                configwrite = True
                config.set(db, 'server', server_public)
    else:
        if not config.has_option(db, 'name'):
            configwrite = True
            config.set(db, 'name', db[3:])
            if not config.has_option(db, 'server'):
                configwrite = True
                config.set(db, 'server', server_desdm)
    if not config.has_option(db, 'port'):
        configwrite = True
        config.set(db, 'port', port_n)

    check = True
    if configwrite:
        check = write_desconfig(desfile, config)
        config.read(desfile)
    if check:
        return config


def write_desconfig(configfile, config_ob):
    """
    Writes configuration file
    """
    try:
        F = open(configfile, 'w')
        F.write(descomment + '\n')
        config_ob.write(F)
        F.flush()
        F.close()
        os.chmod(configfile, 2 ** 8 + 2 ** 7)  # rw-------
        return True
    except:
        print("Problems writing the configuration  file %s" % configfile)
        return False
