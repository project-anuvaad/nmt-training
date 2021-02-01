import logging
import preprocessor.corpus_preprocess as corpus_preprocess
import preprocessor.corpus_tokenize as corpus_tokenize

def preprocess_pipeline(model_type,src_file,tgt_file,epoch,experiment_key):
    try:
        experiment_key = experiment_key or "default"
        preprocessed_data = corpus_preprocess.corpus_preprocessing(src_file,tgt_file,experiment_key)
        preprocessed_data['experiment_key'] = experiment_key

        f_out = pairwise_processing.english_and_hindi(preprocessed_data)

        if model_type == lang_pair['en-hi']['en-to-hi']:
            training_para = {'train_src':f_out['english_encoded_file'],'train_tgt':f_out['hindi_encoded_file'], \
                            'valid_src':f_out['english_dev_encoded_file'],"valid_tgt":f_out['hindi_dev_encoded_file'], \
                            'nmt_processed_data':f_out['nmt_processed_data'],'nmt_model_path':f_out['nmt_model_path'],'epoch':epoch}
        elif model_type == lang_pair['en-hi']['hi-to-en']:
            training_para = {'train_src':f_out['hindi_encoded_file'],'train_tgt':f_out['english_encoded_file'], \
                            'valid_src':f_out['hindi_dev_encoded_file'],"valid_tgt":f_out['english_dev_encoded_file'], \
                            'nmt_processed_data':f_out['nmt_processed_data'],'nmt_model_path':f_out['nmt_model_path'],'epoch':epoch}                                      
        
        onmt_utils.onmt_train(training_para)
    except Exception as e:
        logger.error("error in english_hindi_experiments anuvaad script: {}".format(e))