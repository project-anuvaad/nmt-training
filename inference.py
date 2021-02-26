import utilities.sentencepiece_util as sp 
import utilities.format_handler as format_handler
import os
import sys

DATA_FOLDER = 'data/'

def generate_inference(nmt_model,encoder_model,decoder_model,test_src,key,tgt_lang_code,ref_file):
    try: 
        prediction_folder = os.path.join(DATA_FOLDER, 'prediction')
        if not os.path.exists(prediction_folder):
            os.makedirs(prediction_folder)
            
        test_src_tok = os.path.join(prediction_folder, 'test_src_tok'+'-'+key+'.txt')
        test_src_encoded = os.path.join(prediction_folder, 'test_src_encoded'+'-'+key+'.txt')
        output = os.path.join(prediction_folder, 'output'+'-'+key+'.txt')
        output_decoded = os.path.join(prediction_folder, 'output_decoded'+'-'+key+'.txt')
        output_final = os.path.join(prediction_folder, 'output_final'+'-'+key+'.txt') 

        do_tagging = True
        if do_tagging:
            test_src_tagged = os.path.join(prediction_folder, 'test_src_tagged'+'-'+key+'.txt')
            ref_file_tagged = os.path.join(prediction_folder, 'ref_file_tagged'+'-'+key+'.txt')
            format_handler.tag_number_date_url(test_src,test_src_tagged)
            format_handler.tag_number_date_url(ref_file,ref_file_tagged) 
            test_src = test_src_tagged
            ref_file = ref_file_tagged      
        
        if tgt_lang_code in ['hi','bn','mr','ta','ml','gu','kn','te','pa']:
            os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(test_src, test_src_tok))
            sp.encode_as_pieces(encoder_model,test_src_tok,test_src_encoded)
            os.system('onmt_translate -model {0} -src {1} \
                    -output {2} -verbose -beam_size 5 -gpu 0'.format(nmt_model,test_src_encoded,output))
            sp.decode_as_pieces(decoder_model,output,output_decoded)  
            os.system('python ./tools/indic_detokenize.py {0} {1} {2}'.format(output_decoded,output_final,tgt_lang_code)) 
            
            print("bleu operation begin")
            nmt_out_tok_file = os.path.join(prediction_folder, 'nmt_out_tok_file'+'-'+key+'.txt')
            ref_tok_file = os.path.join(prediction_folder, 'ref_tok_file'+'-'+key+'.txt')
            os.system('python tools/indic_tokenize.py {0} {1} {2}'.format(output_final,nmt_out_tok_file,tgt_lang_code))
            os.system('python tools/indic_tokenize.py {0} {1} {2}'.format(ref_file,ref_tok_file,tgt_lang_code))
            os.system('sacrebleu --tokenize none {0} < {1}'.format(ref_tok_file,nmt_out_tok_file))
            os.system('perl tools/multi-bleu-detok.perl {0} < {1}'.format(ref_file,output_final))
        elif tgt_lang_code =='en':    
            os.system('python ./tools/indic_tokenize.py {0} {1} {2}'.format(test_src,test_src_tok,'bn'))
            sp.encode_as_pieces(encoder_model,test_src_tok,test_src_encoded)
            os.system('onmt_translate -model {0} -src {1} \
                    -output {2} -verbose -beam_size 5 -gpu 0'.format(nmt_model,test_src_encoded,output))
            sp.decode_as_pieces(decoder_model,output,output_decoded)  
            os.system('perl ./tools/detokenize.perl <{0}> {1} -l en'.format(output_decoded,output_final))
            
            print("bleu operation begin")
            nmt_out_tok_file = os.path.join(prediction_folder, 'nmt_out_tok_file'+'-'+key+'.txt')
            ref_tok_file = os.path.join(prediction_folder, 'ref_tok_file'+'-'+key+'.txt')
            os.system('sacrebleu {0} < {1}'.format(ref_file,output_final))
            os.system('perl tools/multi-bleu-detok.perl {0} < {1}'.format(ref_file,output_final))
        
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
    generate_inference(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])     