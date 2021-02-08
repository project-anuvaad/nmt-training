import sentencepiece as spm
import sys
from utilities.logging import init_logger
import os
import config

SENTENCEPIECE_MODEL_DIR = 'model/sentencepiece_models/'
logger = init_logger(config.TRAIN_LOG_FILE)

def train_spm(input_file,prefix,vocab_size,model_type):  
    try:
        user_defined_symbol = 'UuRrLl,NnUuMm'
        spm.SentencePieceTrainer.Train('--input={} --model_prefix={} --vocab_size={} --model_type={} --user_defined_symbols={}'.format(input_file,prefix,vocab_size,model_type,user_defined_symbol))
        os.system('cp {} {}'.format(prefix+'.model',SENTENCEPIECE_MODEL_DIR))
        os.system('cp {} {}'.format(prefix+'.vocab',SENTENCEPIECE_MODEL_DIR))
        os.system('rm -f {0} {1}'.format(prefix+'.model',prefix+'.vocab'))
        logger.info("sp models successfully transfered and removed")
        return
    except Exception as e:
        logger.error("Error during SPM training: ",e)
        logger.error("Unexpected error:", sys.exc_info()[0])
        raise

def encode_as_pieces(load_model,src_file,tgt_file):
    # makes segmenter instance and loads the model file (m.model)
    try:
        sp = spm.SentencePieceProcessor()
        sp.load(load_model)
        with open(src_file) as xh:    
            with open(tgt_file,"w") as outfile:
                xlines= xh.readlines()
        
                for i in range(len(xlines)):
                    encLine = " ".join(sp.encode_as_pieces(xlines[i]))
                    outfile.write((encLine))
                    outfile.write("\n")
    except Exception as e:
        print("something went wrong!: ",e)
        print("Unexpected error:", sys.exc_info()[0])
        raise

def encode_line(load_model,line):
    # makes segmenter instance and loads the model file (m.model)
    try:
        sp = spm.SentencePieceProcessor()
        sp.load(load_model)
        logger.info("encoding using sp model {}".format(load_model))
        return sp.encode_as_pieces(line)
    except:
        logger.info("something went wrong!")
        logger.info("Unexpected error: %s"% sys.exc_info()[0])
        return ""
    

def decode_as_pieces(load_model,src_file,tgt_file):
    try:
        print("decoding")
        spH = spm.SentencePieceProcessor()
        spH.load(load_model)
        with open(src_file) as xh:    
            with open(tgt_file,"w") as outfile:
                xlines= xh.readlines()
        
                for i in range(len(xlines)):     
                    xlines[i] = xlines[i].strip('\n')                            
                    encLine = spH.DecodePieces(xlines[i].split(" "))
                    outfile.write(encLine)
                    outfile.write("\n")
    except Exception as e:
        print("something went wrong!: ",e)
        print("Unexpected error:", sys.exc_info()[0])
        return                    


def decode_line(load_model,line):
    # makes segmenter instance and loads the model file (m.model)
    try:
        sp = spm.SentencePieceProcessor()
        sp.load(load_model)
        if not line.startswith("["):
            line = "["+line
        if not line.endswith("]"):
            line = line+"]"     
        line = line[0]+line[1:-1].replace('[',"")+line[-1] 
        line = line[0]+line[1:-1].replace(']',"")+line[-1]  
        logger.info("decoding using sp model {}".format(load_model))
        if "<unk>" in line:
            line = line.replace("<unk>","")
        return sp.DecodePieces(eval(line))
    except Exception as e:
        logger.error("something went wrong! {}".format(e))
        logger.error("Unexpected error: %s"% sys.exc_info()[0])
        return ""

  
if __name__ == '__main__':
    if sys.argv[1] == "train":
        train_spm(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    elif sys.argv[1] == "encode":
        encode_as_pieces(sys.argv[2],sys.argv[3],sys.argv[4])
    elif sys.argv[1] == "decode":
        decode_as_pieces(sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print("invalid request",sys.argv)
           
