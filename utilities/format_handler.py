import re
from dateutil.parser import parse
import random
import logging


def tag_number_date_url(in_file,out_file):
  try:    
    with open("{0}".format(in_file)) as xh:
      with open("{0}".format(out_file),"w") as zh:
        xlines = xh.readlines() 
        ext_date = list()
        ext_url = list()
        ext_num = list()
        hindi_numbers = ['०', '१', '२', '३','४','५','६','७','८','९','१०','११','१२','१३','१४','१५','१६','१७','१८','१९','२०','२१','२२','२३','२४','२५','२६','२७','२८','२९','३०', \
                         '३१','३२','३३','३४','३५','३६','३७','३८','३९','४०','४१','४२','४३','४४','४५','४६','४७','४८','४९','५०']
        for i in range(len(xlines)):
          resultant_str = list()
          count_date = 0
          count_url = 0
          count_number = 0
          src_num_array = re.findall(r'\d+,\d+,\d+,\d+,\d+|\d+,\d+,\d+,\d+|\d+,\d+,\d+|\d+,\d+|\d+',xlines[i]) 
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
            # ext = [".",",","?","!"]
            # if word.isalpha()== False and word[:-1].isalpha() == False and len(word)>4 and token_is_date(word):
            #   if word.endswith(tuple(ext)):
            #     end_token = word[-1]
            #     word = word[:-1]
            #     if len(word)<7 and (word):    
            #       word = word+end_token
            #     else:
            #       ext_date.append(word)
            #       word = 'DdAaTtEe'+str(count_date)+end_token
            #       count_date +=1
            #   else:
            #     ext_date.append(word)  
            #     word = 'DdAaTtEe'+str(count_date)
            #     count_date +=1
            if token_is_url(word) or token_is_email(word):
              ext_url.append(word)
              word = 'UuRrLl'+str(count_url)
              count_url +=1

            resultant_str.append(word)   
            s = [str(i) for i in resultant_str] 
            res = str(" ".join(s)) 
          zh.write(str(res))
          zh.write('\n')  
        # print("dates: ",ext_date)
        print("url: ",ext_url)
    
  except Exception as e:
    print("in error pass format_handler: ",e)
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
    url = re.findall(r'http[s]?\s*:\s*/\s*/\s*(?:\s*[a-zA-Z]|[0-9]\s*|[$-_@.&+]|\s*[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]\s*))+',token)
    if len(url)>0:
      return True
    else:
      return False  
  except:
    return False

def token_is_email(token):
  try:
    email_pattern = r'[a-zA-Z0-9०-९_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+'
    email = re.findall(email_pattern,token)
    if len(email)>0:
      return True
    else:
      return False  
  except Exception as e:
    return False