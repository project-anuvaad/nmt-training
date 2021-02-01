import re
from dateutil.parser import parse
import random
import logging
from config.regex_pattern import hindi_numbers,patterns


def tag_number_date_url(in_file,out_file):
  try:    
    with open("{0}".format(in_file)) as xh:
      with open("{0}".format(out_file),"w") as zh:
        xlines = xh.readlines() 
        ext_url = list()
        for i in range(len(xlines)):
          resultant_str = list()
          count_url = 0
          count_number = 0
          src_num_array = re.findall(patterns['p12']['regex'],xlines[i]) 
          int_num_array = list(map(lambda y:y.replace(',',''), src_num_array))
          num_array = list(map(int, int_num_array))  
          for k,v in enumerate(src_num_array):
            xlines[i] = xlines[i].replace(v,str(num_array[k]),1)
          num_array.sort(reverse = True)
          for j in num_array:
            xlines[i] = xlines[i].replace(str(j),'NnUuMm'+str(hindi_numbers[count_number]),1)
            count_number +=1
            if count_number >50:
              print("count exceeding 50")
              count_number = 50

          for word in xlines[i].split():
            if token_is_url(word) or token_is_email(word):
              ext_url.append(word)
              word = 'UuRrLl'+str(count_url)
              count_url +=1

            resultant_str.append(word)   
            s = [str(i) for i in resultant_str] 
            res = str(" ".join(s)) 
          zh.write(str(res))
          zh.write('\n')  
        print("url: ",ext_url)
    
  except Exception as e:
    logger.info("Error in corpus/helper_function/format handler, ignoring it-{}".format(e))
    pass

def token_is_date(token):
    try: 
        parse(token, fuzzy=False)
        return True
    except ValueError:
        return False
    except OverflowError:
      print("overflow error while parsing date, treating them as Date tag{}".format(token))
      return True    
    except Exception as e:
      print("error in date parsing for token:{} ".format(token),e)
      return False

def token_is_url(token):
  try:
    url = re.findall(patterns['p13']['regex'],token)
    if len(url)>0:
      return True
    else:
      return False  
  except:
    return False

def token_is_email(token):
  try:
    email_pattern = patterns['p14']['regex']
    email = re.findall(email_pattern,token)
    if len(email)>0:
      return True
    else:
      return False  
  except Exception as e:
    return False