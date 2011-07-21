import psycopg2
import ConfigParser, os
from StringUtils import splitQuoted

# initialize vars
hostname, database, user, password, inputFile, logFile = "", "", "", "", "", ""

'''
  An auction is NOT new if a previous auction can be found that matches all of these criteria:
    1. It is for the same item
    2. It is posted by the same seller
    3. It has the same buyout
    4. It is the same quantity
    5. It expires during the time range
    
    6. The number of auctions 
    
  This WILL exclude additional auctions
'''
def isNew(item):
  seller = item[19]
  time = item[7]
  timeLeft = item[6]
  item = item[22]
  price = item[16]
  ''' 
    Add max and min time left to time. This is the expiry. The expiry for previous auctions must not be in the time range, else
    this might not be a new auction.
    
    timeLeft:
    1 -> Less than 30 mins
    2 -> 30 mins - 2 hours
    3 -> 2 hours - 12 hours
    4 -> 12 hours - 48 hours
  '''
  return True

def loadConfig():
  global hostname, database, user, password, inputFile, logFile 
  config = ConfigParser.RawConfigParser()
  config.read('config.cfg')
  hostname = config.get('Database', 'hostname')
  database = config.get('Database', 'database')
  user = config.get('Database', 'user')
  password = config.get('Database', 'password')
  inputFile = config.get('General', 'inputFile')
  logFile = config.get('General', 'logFile')

def main():
  loadConfig()
  runImport()

def runImport():
  global hostname, database, user, password, inputFile, logFile
  intItemCount=0
  conn = psycopg2.connect('dbname=%s host=%s user=%s password=%s' % (database, hostname, user, password))
  cur = conn.cursor()
  log = open(logFile, 'w')
  f = open(inputFile, 'rU')
  for line in f:
    line = line.lstrip().rstrip()
    if line.lstrip().startswith("\"return"):
      line = line.lstrip('"return {{')
      line = line.rstrip('-- [1]')
      line = line.rstrip('-- [2]')
      items = line.split('},{')
      for item in items:
        intItemCount += 1
        item = item.lstrip().lstrip(r'{')
        item = item.rstrip().rstrip(r'}')
        item = splitQuoted(item, ',')
        counter = 0
        for a in item:
          item[counter] = item[counter].lstrip('\\"').rstrip('\\"')
          log.write(("Item # %s -> %s\n" % (counter, item[counter])))
          if a == "" or a == "nil":
            item[counter] = 0
          counter += 1
        cur.execute("""INSERT INTO auction (link, ilevel, itype, isub, iequip, price, tleft, time, name, texture, count, quality, canuse, ulevel, minbid, mininc, buyout, curbid, amhigh, seller, flag, item_id, suffix, factor, enchant, seed, itemid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (item[0], item[1],item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16], item[17], item[18], item[19], item[20], item[21], item[22], item[23], item[24], item[25], item[26]))
  conn.commit()
  cur.close()
  conn.close()

if __name__ == '__main__':
    main()