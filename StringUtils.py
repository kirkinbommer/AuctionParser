'''
Created on Jul 20, 2011

@author: Kirk
'''
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
