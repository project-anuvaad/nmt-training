import utilities.sentencepiece_util as sp 
import os


def preprocess_test():
    try:
        test_src = 'test/surya.en'
        test_src_tok = 'test/surya_tok.en'
        test_src_encoded = 'test/surya_encoded.en'
        output = 'test/surya_out.bn'
        output_decoded = 'test/surya_out_decoded.bn'
        output_final = 'test/surya_out_final.bn'
        nmt_model = 'test/model_test_en-to-bn-1_2021-02-02_model_step_200000.pt'
        encoder_model = 'test/en_test_en-to-bn-1-2021-02-02-24k.model'
        decoder_model = 'test/bn_test_en-to-bn-1-2021-02-02-24k.model'
        os.system('perl ./tools/tokenizer.perl <{0}> {1}'.format(test_src, test_src_tok))
        sp.encode_as_pieces(encoder_model,test_src_tok,test_src_encoded)
        os.system('onmt_translate -model {0} -src {1} \
                  -output {2} -verbose -beam_size 5'.format(nmt_model,test_src_encoded,output))
        sp.decode_as_pieces(decoder_model,output,output_decoded)  
        os.system('python ./tools/indic_detokenize.py {0} {1} hi'.format(output_decoded,output_final))                
        
    except Exception as e:
        print(e)    
        
preprocess_test()        