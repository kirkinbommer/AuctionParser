import psycopg2

def splitQuoted(input, char=','):
  inQuote = False
  output = []
  itemCount = 0
  output.append("")
  for c in input:
    if c == ',':
      if inQuote:
        output[itemCount] += c
      else:
        itemCount += 1
        output.append("")
    elif c == '\"':
      if inQuote:
        inQuote = False
      else:
        inQuote = True
    else:
      output[itemCount] += c
  return output

intItemCount=0
conn = psycopg2.connect("dbname=auction host=localhost user=postgres password=postgres")
cur = conn.cursor()
log = open('parseAuc.log', 'w')
with open('Auc-ScanData.lua', 'rU') as f:
  for line in f:
    if line.lstrip().startswith("\"return"):
      line = line.lstrip().lstrip('"return {{')
      line = line.rstrip().rstrip('-- [1]')
      line = line.rstrip().rstrip('-- [2]')
      items = line.split('},{')
      for item in items:
        intItemCount += 1
        item = item.lstrip().lstrip(r'{')
        item = item.rstrip().rstrip(r'}')
        attr = splitQuoted(item, ',')
        counter = 0
        for a in attr:
          attr[counter] = attr[counter].lstrip('\\"').rstrip('\\"')
          log.write(("Item # %s -> %s\n" % (counter, attr[counter])))
          if a == "" or a == "nil":
            attr[counter] = 0
          counter += 1
        cur.execute("""INSERT INTO auction (link, ilevel, itype, isub, iequip, price, tleft, time, name, texture, count, quality, canuse, ulevel, minbid, mininc, buyout, curbid, amhigh, seller, flag, item_id, suffix, factor, enchant, seed, itemid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (attr[0], attr[1],attr[2], attr[3], attr[4], attr[5], attr[6], attr[7], attr[8], attr[9], attr[10], attr[11], attr[12], attr[13], attr[14], attr[15], attr[16], attr[17], attr[18], attr[19], attr[20], attr[21], attr[22], attr[23], attr[24], attr[25], attr[26]))
conn.commit()
cur.close()
conn.close()
