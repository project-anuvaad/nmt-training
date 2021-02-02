from utilities.logging import init_logger
import preprocessor.corpus_preprocess as corpus_preprocess
import preprocessor.corpus_tokenize as corpus_tokenize
import sys
import config

logger = init_logger(config.TRAIN_LOG_FILE)

def preprocess_pipeline(src_lang_code,tgt_lang_code,src_file,tgt_file,experiment_key):
    try:
        logger.info("Initiate training on {} and {} for exp:{}".format(src_file,tgt_file,experiment_key))
        experiment_key = experiment_key or "default"
        preprocessed_data = corpus_preprocess.corpus_preprocessing(src_file,tgt_file,experiment_key)
        preprocessed_data['experiment_key'] = experiment_key
        preprocessed_data['src_lang'],preprocessed_data['tgt_lang'] = src_lang_code,tgt_lang_code

        f_out = corpus_tokenize.corpus_tokenizer(preprocessed_data)
        training_params = {'train_src':f_out['src_tokenized_file'],'train_tgt':f_out['tgt_tokenized_file'], \
                         'valid_src':f_out['src_dev_tokenized_file'],"valid_tgt":f_out['tgt_dev_tokenized_file']}                           
        
        logger.info("Training files: {}".format(training_params))
    except Exception as e:
        logger.error("error in preprocess_pipeline: {}".format(e))
        

if __name__ == '__main__':
    logger.info("*****Preprocess.py******")
    preprocess_pipeline(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
          