import logging
import uuid
import os
import utilities.format_handler as format_handler
import utilities.file_operation as file_operation

DATA_FOLDER = 'data/'

def corpus_preprocessing(src_file,tgt_file,key):
    try:
        tab_sep_out_file = os.path.join(DATA_FOLDER, 'tab_sep_corpus'+'-'+key+'.txt')
        tab_sep_out_file_no_duplicate = os.path.join(DATA_FOLDER, 'tab_sep_corpus_no_duplicate'+'-'+key+'.txt')
        shuffled_tab_sep_file = os.path.join(DATA_FOLDER, 'shuffled_tab_sep_file'+'-'+key+'.txt')
        train_file = os.path.join(DATA_FOLDER, 'train_file'+'-'+key+'.txt')
        dev_file = os.path.join(DATA_FOLDER, 'dev_file'+'-'+key+'.txt')
        eng_separated = os.path.join(DATA_FOLDER, 'eng_train_separated'+'-'+key+'.txt')
        hindi_separated = os.path.join(DATA_FOLDER, 'hindi_train_separated'+'-'+key+'.txt')
        eng_dev_separated = os.path.join(DATA_FOLDER, 'eng_dev_separated'+'-'+key+'.txt')
        hindi_dev_separated = os.path.join(DATA_FOLDER, 'hindi_dev_separated'+'-'+key+'.txt')
        
        english_tagged = os.path.join(DATA_FOLDER, 'eng_train_corpus_final'+'-'+key+'.txt')
        hindi_tagged = os.path.join(DATA_FOLDER, 'hindi_train_corpus_final'+'-'+key+'.txt')
        dev_english_tagged = os.path.join(DATA_FOLDER, 'english_dev_final'+'-'+key+'.txt')
        dev_hindi_tagged = os.path.join(DATA_FOLDER, 'hindi_dev_final'+'-'+key+'.txt')             

        file_operation.tab_separated_parllel_corpus(tgt_file, src_file, tab_sep_out_file)
        logger.info("tab separated corpus created")
        logger.info(os.system('wc -l {}'.format(tab_sep_out_file)))
        file_operation.drop_duplicate(tab_sep_out_file, tab_sep_out_file_no_duplicate)
        logger.info("duplicates removed from combined corpus")
        logger.info(os.system('wc -l {}'.format(tab_sep_out_file_no_duplicate)))
        
        file_operation.shuffle_file(tab_sep_out_file_no_duplicate,shuffled_tab_sep_file)
        logger.info("tab_sep_file_shuffled_successfully!")

        file_operation.split_into_train_validation(shuffled_tab_sep_file,train_file,dev_file,0.995)
        logger.info("splitted file into train and validation set")

        file_operation.separate_corpus(0, train_file, eng_separated)
        file_operation.separate_corpus(1, train_file, hindi_separated)
        file_operation.separate_corpus(0, dev_file, eng_dev_separated)
        file_operation.separate_corpus(1, dev_file, hindi_dev_separated)
        logger.info("corpus separated into src and tgt for training and validation")

        format_handler.tag_number_date_url(eng_separated, english_tagged)
        format_handler.tag_number_date_url(hindi_separated, hindi_tagged)
        format_handler.tag_number_date_url(eng_dev_separated, dev_english_tagged)
        format_handler.tag_number_date_url(hindi_dev_separated, dev_hindi_tagged)

        logger.info("url,number tagging done")

        os.system('rm -f {0} {1} {2} {3} {4} {5} {6} {7} {8}'.format(tab_sep_out_file,tab_sep_out_file_no_duplicate,shuffled_tab_sep_file,\
                  train_file,dev_file,eng_separated,hindi_separated,eng_dev_separated,hindi_dev_separated))
        logger.info("intermediate files are removed successfully: in corpus/scripts/en-hi") 

        return {'ENGLISH_TRAIN_FILE':english_tagged,'HINDI_TRAIN_FILE':hindi_tagged, 'DEV_ENGLISH':dev_english_tagged,'DEV_HINDI':dev_hindi_tagged, \
               }

    except Exception as e:
        logger.error("error in english_hindi_experiments corpus/scripts- {}".format(e))