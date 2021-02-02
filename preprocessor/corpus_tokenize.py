from utilities.logging import init_logger
import os
import utilities.sentencepiece_util as sp
import datetime
import config

DATA_FOLDER = 'data/'
LANGUAGE_CODE = {'indic':['hi','bn','mr','ta','ml','gu','kn','te','pa'],'english':'en'}
date_now = datetime.datetime.now().strftime('%Y-%m-%d')
logger = init_logger(config.TRAIN_LOG_FILE)

def corpus_tokenizer(inputs):
    try:
        experiment_key = inputs['experiment_key']
        src_lang,tgt_lang = inputs['src_lang'],inputs['tgt_lang']
        sp_model_prefix_src = '{}_{}-{}-24k'.format(src_lang,experiment_key,date_now)
        sp_model_prefix_tgt = '{}_{}-{}-24k'.format(tgt_lang,experiment_key,date_now)
        src_tokenized_file = os.path.join(DATA_FOLDER, 'src_train_tok'+'-'+experiment_key+'.txt')
        src_dev_tokenized_file = os.path.join(DATA_FOLDER, 'src_dev_tok'+'-'+experiment_key+'.txt')
        tgt_tokenized_file = os.path.join(DATA_FOLDER, 'tgt_train_tok'+'-'+experiment_key+'.txt')
        tgt_dev_tokenized_file = os.path.join(DATA_FOLDER, 'tgt_dev_tok'+'-'+experiment_key+'.txt')

        logger.info("corpus_tokenizer preprocessing starting for exp:{}".format(experiment_key))
        if src_lang in LANGUAGE_CODE['indic'] and tgt_lang == LANGUAGE_CODE['english']:
            logger.info("src:indic || tgt:english")
            indic_lang_tokenizer(src_lang, inputs['SRC_TRAIN_FILE'],src_tokenized_file)
            indic_lang_tokenizer(src_lang, inputs['DEV_SRC'],src_dev_tokenized_file)
            eng_lang_tokenizer(inputs['TGT_TRAIN_FILE'],tgt_tokenized_file) 
            eng_lang_tokenizer(inputs['DEV_TGT'],tgt_dev_tokenized_file) 
            
        elif src_lang == LANGUAGE_CODE['english'] and tgt_lang in LANGUAGE_CODE['indic']:
            logger.info("src:english || tgt:indic")  
            indic_lang_tokenizer(tgt_lang,inputs['TGT_TRAIN_FILE'],tgt_tokenized_file)
            indic_lang_tokenizer(tgt_lang,inputs['DEV_TGT'],tgt_dev_tokenized_file)
            eng_lang_tokenizer(inputs['SRC_TRAIN_FILE'],src_tokenized_file) 
            eng_lang_tokenizer(inputs['DEV_SRC'],src_dev_tokenized_file) 
            
        logger.info("Tokenization finished!")
        sp.train_spm(src_tokenized_file,sp_model_prefix_src, 24000, 'bpe')
        logger.info("corpus_tokenizer preprocessing,sentencepiece model src trained")
        sp.train_spm(tgt_tokenized_file,sp_model_prefix_tgt, 24000, 'bpe')
        logger.info("corpus_tokenizer preprocessing,sentencepiece model tgt trained")

        os.system('rm -f {0} {1} {2} {3}'.format(inputs['SRC_TRAIN_FILE'],inputs['DEV_SRC'],inputs['TGT_TRAIN_FILE'],inputs['DEV_TGT']))
        logger.info("Removed intermediate files, corpus_tokenizer preprocessing finished!")

        return {"src_tokenized_file":src_tokenized_file,"tgt_tokenized_file":tgt_tokenized_file,"src_dev_tokenized_file":src_dev_tokenized_file, \
               "tgt_dev_tokenized_file":tgt_dev_tokenized_file}

    except Exception as e:
        logger.info("error in corpus_tokenizer: {}".format(e))
        
def indic_lang_tokenizer(lang_code, input_file,output_file):
    '''
    Using Indic tokenizer for tokenizing Indic languages
    '''
    os.system('python ./tools/indic_tokenize.py {0} {1} {2}'.format(input_file,output_file,lang_code))
    logger.info("indic_lang_tokenization finished!")

def eng_lang_tokenizer(input_file,output_file):    
    '''
    Using Moses perl script to tokenize english sentences
    '''    
    os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(input_file, output_file))
    logger.info("eng_lang_tokenization finished!")
        