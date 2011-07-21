import ConfigParser

def main():
    config = ConfigParser.RawConfigParser()
    config.add_section('Database')
    config.set('Database', 'hostname', 'localhost')
    config.set('Database', 'database', 'auction')
    config.set('Database', 'user', 'postgres')
    config.set('Database', 'password', 'postgres')
    config.add_section('General')
    config.set('General', 'inputFile', 'test.lua')
    config.set('General', 'logFile', 'auction.log')
    
    configfile = open('config.cfg', 'wb')
    config.write(configfile)

if __name__ == '__main__':
    main()