def tokenizer(inputs):
    try:
        experiment_key = inputs['experiment_key']
        unique_id = inputs['unique_id']
        sp_model_prefix_hindi = 'hi_{}-{}-24k'.format(experiment_key,date_now)
        sp_model_prefix_english = 'en_{}-{}-24k'.format(experiment_key,date_now)
        model_intermediate_folder = os.path.join(INTERMEDIATE_DATA_LOCATION, 'english_hindi')
        model_master_train_folder = os.path.join(TRAIN_DEV_TEST_DATA_LOCATION, 'english_hindi')
        nmt_model_path = os.path.join(NMT_MODEL_DIR, 'english_hindi','model_en-hi_{}_{}-model'.format(experiment_key,date_now))
        if not any([os.path.exists(model_intermediate_folder),os.path.exists(model_master_train_folder),os.path.exists(os.path.join(NMT_MODEL_DIR, 'english_hindi'))]):
            os.makedirs(model_intermediate_folder)
            os.makedirs(model_master_train_folder)
            os.makedirs(os.path.join(NMT_MODEL_DIR, 'english_hindi'))
            logger.info("folder created at {}".format(model_intermediate_folder))
        hindi_tokenized_file = os.path.join(model_intermediate_folder, 'hindi_train_tok'+unique_id+'.txt')
        hindi_dev_tokenized_file = os.path.join(model_intermediate_folder, 'hindi_dev_tok'+unique_id+'.txt')
        english_tokenized_file = os.path.join(model_intermediate_folder, 'english_train_tok'+unique_id+'.txt')
        english_dev_tokenized_file = os.path.join(model_intermediate_folder, 'english_dev_tok'+unique_id+'.txt')
        hindi_encoded_file = os.path.join(model_master_train_folder, 'hindi_train_final'+unique_id+'.txt')
        hindi_dev_encoded_file = os.path.join(model_master_train_folder, 'hindi_dev_final'+unique_id+'.txt')
        english_encoded_file = os.path.join(model_master_train_folder, 'english_train_final'+unique_id+'.txt')
        english_dev_encoded_file = os.path.join(model_master_train_folder, 'english_dev_final'+unique_id+'.txt')
        nmt_processed_data = os.path.join(model_master_train_folder, 'processed_data_{}_{}'.format(experiment_key,date_now))

        logger.info("Eng-hin pairwise preprocessing, startting for exp:{}".format(experiment_key))
        os.system('python ./tools/indic_tokenize.py {0} {1} hi'.format(inputs['HINDI_TRAIN_FILE'], hindi_tokenized_file))
        os.system('python ./tools/indic_tokenize.py {0} {1} hi'.format(inputs['DEV_HINDI'], hindi_dev_tokenized_file))
        logger.info("Eng-hin pairwise preprocessing, hindi train,dev,test corpus tokenized")
        os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(inputs['ENGLISH_TRAIN_FILE'], english_tokenized_file))
        os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(inputs['DEV_ENGLISH'], english_dev_tokenized_file))
        logger.info("Eng-hin pairwise preprocessing, english train,dev,test corpus tokenized")
        sp.train_spm(hindi_tokenized_file,sp_model_prefix_hindi, 24000, 'bpe')
        logger.info("Eng-hin pairwise preprocessing,sentencepiece model hindi trained")
        sp.train_spm(english_tokenized_file,sp_model_prefix_english, 24000, 'bpe')
        logger.info("Eng-hin pairwise preprocessing,sentencepiece model english trained")

        # sp.encode_as_pieces(os.path.join(SENTENCEPIECE_MODEL_DIR, (sp_model_prefix_hindi+'.model')),hindi_tokenized_file,hindi_encoded_file)
        # sp.encode_as_pieces(os.path.join(SENTENCEPIECE_MODEL_DIR, (sp_model_prefix_hindi+'.model')),hindi_dev_tokenized_file,hindi_dev_encoded_file)
        # logger.info("hindi-train,dev,test encoded and final stored in data folder")
        # sp.encode_as_pieces(os.path.join(SENTENCEPIECE_MODEL_DIR, (sp_model_prefix_english+'.model')),english_tokenized_file,english_encoded_file)
        # sp.encode_as_pieces(os.path.join(SENTENCEPIECE_MODEL_DIR, (sp_model_prefix_english+'.model')),english_dev_tokenized_file,english_dev_encoded_file)
        # logger.info("english-train,dev,test file encoded and final stored in data folder")

        os.system('rm -f {0} {1} {2} {3} {4} {5} {6} {7}'.format(hindi_tokenized_file,hindi_dev_tokenized_file,english_tokenized_file,english_dev_tokenized_file,\
                   inputs['HINDI_TRAIN_FILE'],inputs['DEV_HINDI'],inputs['ENGLISH_TRAIN_FILE'],inputs['DEV_ENGLISH']))
        logger.info("removed intermediate files: pairwise preporcessing: eng-hindi")

        os.system('rm- f {0} {1} {2} {3}'.format(english_test_Gen_encoded_file,english_test_LC_encoded_file,hindi_test_Gen_encoded_file,hindi_test_LC_encoded_file))

        return {"english_encoded_file":english_encoded_file,"hindi_encoded_file":hindi_encoded_file,"english_dev_encoded_file":english_dev_encoded_file, \
               "hindi_dev_encoded_file":hindi_dev_encoded_file,"nmt_processed_data":nmt_processed_data,"nmt_model_path":nmt_model_path}

    except Exception as e:
        print(e)
        logger.info("error in english_hindi anuvaad script: {}".format(e))