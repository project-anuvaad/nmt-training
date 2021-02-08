from utilities.logging import init_logger
import os
import utilities.format_handler as format_handler
import utilities.file_operation as file_operation
import config

DATA_FOLDER = 'data/'
logger = init_logger(config.TRAIN_LOG_FILE)

def corpus_preprocessing(src_file,tgt_file,src_dev_file,tgt_dev_file,key):
    try:
        tab_sep_out_file = os.path.join(DATA_FOLDER, 'tab_sep_corpus'+'-'+key+'.txt')
        tab_sep_out_file_no_duplicate = os.path.join(DATA_FOLDER, 'tab_sep_corpus_no_duplicate'+'-'+key+'.txt')
        shuffled_tab_sep_file = os.path.join(DATA_FOLDER, 'shuffled_tab_sep_file'+'-'+key+'.txt')
        src_seperated = os.path.join(DATA_FOLDER, 'src_train_separated'+'-'+key+'.txt')
        tgt_seperated = os.path.join(DATA_FOLDER, 'tgt_train_separated'+'-'+key+'.txt')
        
        src_tagged = os.path.join(DATA_FOLDER, 'src_train_tagged_final'+'-'+key+'.txt')
        tgt_tagged = os.path.join(DATA_FOLDER, 'tgt_train_tagged_final'+'-'+key+'.txt')
        dev_src_tagged = os.path.join(DATA_FOLDER, 'src_dev_tagged_final'+'-'+key+'.txt')
        dev_tgt_tagged = os.path.join(DATA_FOLDER, 'tgt_dev_tagged_final'+'-'+key+'.txt')             

        file_operation.tab_separated_parllel_corpus(tgt_file, src_file, tab_sep_out_file)
        logger.info("tab separated corpus created")
        logger.info(os.system('wc -l {}'.format(tab_sep_out_file)))
        file_operation.drop_duplicate(tab_sep_out_file, tab_sep_out_file_no_duplicate)
        logger.info("duplicates removed from combined corpus")
        logger.info(os.system('wc -l {}'.format(tab_sep_out_file_no_duplicate)))
        
        file_operation.shuffle_file(tab_sep_out_file_no_duplicate,shuffled_tab_sep_file)
        logger.info("tab_sep_file_shuffled_successfully!")

        file_operation.separate_corpus(0, shuffled_tab_sep_file, src_seperated)
        file_operation.separate_corpus(1, shuffled_tab_sep_file, tgt_seperated)
        logger.info("corpus separated into src and tgt for training and validation")

        format_handler.tag_number_date_url(src_seperated, src_tagged)
        format_handler.tag_number_date_url(tgt_seperated, tgt_tagged)
        format_handler.tag_number_date_url(src_dev_file, dev_src_tagged)
        format_handler.tag_number_date_url(tgt_dev_file, dev_tgt_tagged)

        logger.info("url,number tagging done")

        os.system('rm -f {0} {1} {2} {3} {4}'.format(tab_sep_out_file,tab_sep_out_file_no_duplicate,shuffled_tab_sep_file,\
                  src_seperated,tgt_seperated))
        logger.info("intermediate files are removed successfully,corpus_preprocessing") 

        return {'SRC_TRAIN_FILE':src_tagged,'TGT_TRAIN_FILE':tgt_tagged, 'DEV_SRC':dev_src_tagged,'DEV_TGT':dev_tgt_tagged }

    except Exception as e:
        logger.error("error in corpus_preprocessing {}".format(e))
        
        
def build_train_dev_set():
    '''
    Creates train and dev set by spliting corpus into certain ratio
    '''        
    file_operation.split_into_train_validation(shuffled_tab_sep_file,train_file,dev_file,0.995)
    logger.info("splitted file into train and validation set")
    
def corpus_shuffling(src_file,tgt_file,key):
    '''
    Performs only corpus shuffling
    '''
    tab_sep_out_file = os.path.join(DATA_FOLDER, 'tab_sep_corpus'+'-'+key+'.txt')
    shuffled_tab_sep_file = os.path.join(DATA_FOLDER, 'shuffled_tab_sep_file'+'-'+key+'.txt')
    src_seperated = os.path.join(DATA_FOLDER, 'src_train_separated'+'-'+key+'.txt')
    tgt_seperated = os.path.join(DATA_FOLDER, 'tgt_train_separated'+'-'+key+'.txt')
    
    file_operation.tab_separated_parllel_corpus(tgt_file, src_file, tab_sep_out_file)
    logger.info("tab separated corpus created")
    logger.info(os.system('wc -l {}'.format(tab_sep_out_file)))
    
    file_operation.shuffle_file(tab_sep_out_file,shuffled_tab_sep_file)
    logger.info("tab_sep_file_shuffled_successfully!")

    file_operation.separate_corpus(0, shuffled_tab_sep_file, src_seperated)
    file_operation.separate_corpus(1, shuffled_tab_sep_file, tgt_seperated)
    logger.info("corpus separated into src and tgt for training after shuffling")
    
    os.system('rm -f {0} {1}'.format(tab_sep_out_file,shuffled_tab_sep_file))
    logger.info("intermediate files are removed successfully,corpus_shuffling") 
    
    return {'SRC_TRAIN_FILE':src_seperated,'TGT_TRAIN_FILE':tgt_seperated}
        