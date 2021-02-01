import random

## below is for dropping duplicate from text file
def drop_duplicate(inFile,outFile):
    lines_seen = set() # holds lines already seen
    outfile = open("{0}".format(outFile), "w")
    for line in open("{0}".format(inFile), "r"):
        if line not in lines_seen: # not a duplicate
           outfile.write(line)
           lines_seen.add(line)
    outfile.close()

## separation into master corpus src and tgt for training. After this tokenization needs to be done(indic nlp, moses),then feed into OpenNMT
def separate_corpus(col_num,inFile,outFile):
    outfile = open("{0}".format(outFile), "w")
    delimiter = "\t"
    for line in open("{0}".format(inFile), "r"):
        # col_data.append(f.readline().split(delimiter)[col_num])
        outfile.write(str(line.split(delimiter)[col_num].replace('\n','')))
        outfile.write("\n")    
    outfile.close()

" remove duplicate and whitespaces from parallel corpus built after merging step "
def tab_separated_parllel_corpus(mono_corpus1,mono_corpus2,out_file):
    with open("{0}".format(mono_corpus1)) as xh:
      with open("{0}".format(mono_corpus2)) as yh:
        with open("{0}".format(out_file),"w") as zh:
          #Read first file
          xlines = xh.readlines()
          #Read second file
          ylines = yh.readlines()
      
          #Write to third file
          for i in range(len(xlines)):
            line = ylines[i].strip() + '\t' + xlines[i]
            zh.write(line)

def split_into_train_validation(input_file,train_file,validation_file,percentage):
  try:
    isShuffle=True
    random.seed(123)
    outfile_train = open("{0}".format(train_file), "w") 
    outfile_val = open("{0}".format(validation_file), "w")
    with open(input_file, 'r',encoding="utf-8") as fin:
      nLines = sum(1 for line in fin)
      fin.seek(0)
      nTrain = int(nLines*percentage)
      nValid = nLines - nTrain
      i = 0
      for line in fin:
        r = random.random() if isShuffle else 0 
        if (i < nTrain and r < percentage) or (nLines - i > nValid):
          outfile_train.write(line)
          i += 1
        else:
          outfile_val.write(line)
  except Exception as e:
    print(e)

def shuffle_file(in_file,out_file):
  "for shuffling a single file. Current use case is to shuffle tab sep file in scripts"
  try:
    lines = open(in_file).readlines()
    random.shuffle(lines)
    open(out_file, 'w').writelines(lines)
    print("shuffling successful")
    
  except Exception as e:
    print("Error: while shuffling file,in format_handler",e)