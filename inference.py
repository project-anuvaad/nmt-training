import utilities.sentencepiece_util as sp 
import os

DATA_FOLDER = 'data/'

def generate_inference(nmt_model,encoder_model,decoder_model,test_src,key,tgt_lang_code):
    try: 
        prediction_folder = os.path.join(DATA_FOLDER, 'prediction')
        if not os.path.exists(prediction_folder):
            os.makedirs(prediction_folder)
            
        test_src_tok = os.path.join(prediction_folder, 'test_src_tok'+'-'+key+'.txt')
        test_src_encoded = os.path.join(prediction_folder, 'test_src_encoded'+'-'+key+'.txt')
        output = os.path.join(prediction_folder, 'output'+'-'+key+'.txt')
        output_decoded = os.path.join(prediction_folder, 'output_decoded'+'-'+key+'.txt')
        output_final = os.path.join(prediction_folder, 'output_final'+'-'+key+'.txt')        
        
        os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(test_src, test_src_tok))
        sp.encode_as_pieces(encoder_model,test_src_tok,test_src_encoded)
        os.system('onmt_translate -model {0} -src {1} \
                  -output {2} -verbose -beam_size 5'.format(nmt_model,test_src_encoded,output))
        sp.decode_as_pieces(decoder_model,output,output_decoded)  
        os.system('python ./tools/indic_detokenize.py {0} {1} {2}'.format(output_decoded,output_final,tgt_lang_code))                
        
    except Exception as e:
        print(e)    

# nmt_model = 'test/model_test_en-to-bn-1_2021-02-02_model_step_200000.pt'
# encoder_model = 'test/en_test_en-to-bn-1-2021-02-02-24k.model'
# decoder_model = 'test/bn_test_en-to-bn-1-2021-02-02-24k.model'
# test_src = 'test/surya.en'
# key = "en-ta"
# tgt_lang_code = 'hi'
        
# generate_inference(nmt_model,encoder_model,decoder_model,test_src,key,tgt_lang_code)   


if __name__ == '__main__':
    generate_inference(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])     