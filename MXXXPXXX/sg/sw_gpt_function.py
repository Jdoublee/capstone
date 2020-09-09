#version 2020_05_16(1)
#version 2020_05_17(2)
print('server loading...')
'''
    1. 기본 package
'''

import os
import sys
import random
import torch
from gluonnlp.data import SentencepieceTokenizer
import re
'''
    2. KoGPT2 package
'''

from minegpt2.kogpt2.utils import get_tokenizer
from minegpt2.kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model

# from kogpt2.utils import get_tokenizer
# from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
'''
3. 함수에서 사용할 전역변수 tok_path, tok, model, vocab
'''
# sk에서 제공하는 50000단어 모델로 변수 설정
# 문장 속도 최적화를 위해, 서버 실행시 전역 변수로 사용하기 위해서
# django App 생성 후 그 폴더 내부에 저장
# @@@views.py에 import 하면 이 파일은 서버 실행 될때 실행된다.@@@
# (app내부가 아닌 py 파일은 서버 실행시 모두 실행되지 않음)
tok_path = get_tokenizer()
tok = SentencepieceTokenizer(tok_path, 0, 0)

# 1) model, vocab 파일의 경우 setup.py 실행시
# kogpt2가 파이썬 내장 모듈로 설정되어 파이썬 설치 경로에 존재
# 2) sys.path.append('~~~')로 폴더를 직접 추가 한 경우
# 파이썬이 사용자 폴더를 참조, 사용자 폴더에 존재
# 3) 한번 다운로드 후 특별한 일이 없는 한 다운하지 않고
# 다운되어 있는 파일을 사용 (using cached model)
model, vocab = get_pytorch_kogpt2_model()
'''
#   4. fine turning한 것을 모델에 적용하기
'''


# load_path는 각각 local에서 tar파일을 저장한 곳으로
# 다르게 지정한다.
# 여러 fineturing 파일을 적용하는 법은 아직 하지 않았다.
def adaptFineTurning(string):
    load_path = '/home/park/data/'
    load_path = load_path + string + '.tar'
    print(load_path)
    device = torch.device('cpu')
    checkpoint = torch.load(load_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])


'''
    5. 정의된 함수들
    단어 추천 함수 : words_list, context_words_list, context_words_list2
    문장 생성 함수 : step_by_step_generate, serveral_sentence_generate, one_sentence_generate,

    확률 계산은 모르겠다.
    ***주의사항***
    @@@!!! 모두 장고에 맞게 추후 수정 필요!!!@@@
    (추천 단어 보여주기,,, 실시간 사용자의 단어 입력 받고 처리 하기 등등..)
    (터미널에서 이루어지기 때문에 서버 실행 전에는 input() 비활성화하고 실험할때만.)
'''


# kogpt2 단어 예측의 경우 마지막 단어만 이용하여 예측하는 것이 아님
# 지금까지 입력된 모든 단어들을 이용하여 다음 단어 예측
# 즉 '중국의'+'경제개혁은' -> '시진핑'을 가장 추천
# '경제개혁은' -> '시진핑'이 아닌 다른 단어를 추천
# 그러나 문맥에 상관 없이 한 단어 or 끝나지 않은 문장을 입력했을때에도
# 다음 단어를 추천해 줄 수 있는 함수를 만듬 필요없지만 필요할수도 있을거 같아서
# 한 단어에 대한 다음 단어 추천 words 는 str, ret은 list{str}
def words_list(words):
    ret = list()
    toked = tok(words)
    cnt = len(toked) - 1
    input_ids = torch.tensor([
        vocab[vocab.bos_token],
    ] + vocab[toked]).unsqueeze(0)
    pred = model(input_ids)[0]
    print(cnt)
    sort = torch.argsort(-pred, axis=-1)[0]
    for i in range(0, 10):
        a = sort[cnt][i].squeeze().tolist()
        b = sort[cnt + 1][i].squeeze().tolist()
        gen = vocab.to_tokens([b])
        ret.append(gen)

    return ret


# 문맥에 맞는 추천 단어 생성
# 위 words_list와 다르게 문맥을 전달해주어야함
# pred = 단순 str이 아닌 model 변수, ret은 list{str}
def context_words_list(pred):
    ret = list()  # 추천 단어를 담을 list
    _pred = pred  # 전달 받은 입력된 단어들,문맥

    cnt = len(_pred[0]) - 2  # 여러 단어를 입력했을 수 있으므로 반드시 필요

    sort = torch.argsort(-_pred, axis=-1)[0]  # 확률이 큰 기준으로 정렬
    for i in range(0, 10):
        a = sort[cnt][i].squeeze().tolist()
        b = sort[cnt + 1][i].squeeze().tolist()
        h = _pred[0][cnt + 1][b].squeeze().tolist()  # 확률 야매
        gen = vocab.to_tokens([b])  # 하나의 추천 단어
        gen[0] = gen[0].replace('▁', ' ')
        ret.append([gen, round(h / 2, 2)])

    return ret


# tensor 형태로 변환하지 않고str만 전해줘도 문맥파악 후 추천 단어
def context_words_list2(words):
    ret = list()  # 추천 단어를 담을 list

    toked = tok(words)
    input_ids = torch.tensor([
        vocab[vocab.bos_token],
    ] + vocab[toked]).unsqueeze(0)
    _pred = model(input_ids)[0]

    cnt = len(_pred[0]) - 2  # 여러 단어를 입력했을 수 있으므로 반드시 필요

    sort = torch.argsort(-_pred, axis=-1)[0]  # 확률이 큰 기준으로 정렬
    for i in range(0, 10):
        a = sort[cnt][i].squeeze().tolist()
        b = sort[cnt + 1][i].squeeze().tolist()
        h = _pred[0][cnt + 1][b].squeeze().tolist()  # 확률 야매
        gen = vocab.to_tokens([b])  # 하나의 추천 단어
        gen[0] = gen[0].replace('▁', ' ')
        ret.append([gen, round(h / 2, 2)])

    return ret


# 문맥에 맞는 추천 단어 생성 함수(context_words_list())를 사용
# 사용자가 추천단어를 보고 원하는(추천단어가 아니어도됨) 여러 단어를 입력
# 사용자가 한 문장을(여러 문장을) 끝내면 str로 반환
# 현재 추천 단어는 터미널에 print됨
def step_by_step_generate():
    sent = input('입력 :: ')
    toked = tok(sent)

    while 1:
        input_ids = torch.tensor([
            vocab[vocab.bos_token],
        ] + vocab[toked]).unsqueeze(0)
        pred = model(input_ids)[0]

        # 추천 단어 보여주기, 문맥 적용
        print(context_words_list(pred))

        # 입력은 사용자가 하고 싶은거 하기
        # _은 스페이스바임. 추천그대로 하려면 반드시 입력할것
        gen = input('입력 :: ')

        # 사용자가 !end를 입력한경우 종료되게 설정
        if gen == '!end' or gen == '</s>':
            print('end')
            break

        sent += gen.replace('▁', ' ')
        toked = tok(sent)

    print(sent)
    return sent


# 두개 이상의 문장을 생성
# return은 str의 리스트
# 추천 단어 사용 불가
def serveral_sentence_generate(sent='일본은', generate_num=5):
    #sent = input('입력 : ')
    ret_list = list()
    toked = tok(sent)
    input_ids = torch.tensor([
        vocab[vocab.bos_token],
    ] + vocab[toked]).unsqueeze(0)

    # 학습한 모델 적용
    # adaptFineTurning('333')

    # do_sample True 랜덤 생성
    # num_return_sequences 생성할 문장 개수

    outputs = model.generate(input_ids=input_ids,
                             max_length=300,
                             min_length=200,
                             repetition_penalty=1.0,
                             do_sample=True,
                             num_return_sequences=generate_num,
                             eos_token_id=0,
                             pad_token_id=3)

    for i in range(generate_num):
        toked = vocab.to_tokens(outputs[i].squeeze().tolist())
        ret = re.sub(r'(<s>|</s>)', '', ''.join(toked).replace('▁',
                                                               ' ').strip())
        ret = ret.replace('<pad>', '')
        ret = ret.replace('<unk>', '')
        ret += '\n\n'
        ret_list.append(ret)

    return ret_list


# 한 문장을 만들어낸다 return은 str
# option 설정 do_sample=False -> 항상 같은 문장 만듬
# 여러 문장 만들어내는 함수와 toked 부분이 다름
# 추천 단어 사용 불가


def one_sentence_generate(sent='한국은', do_sample=True):
    #sent = input('입력 : ')

    toked = tok(sent)
    sent_cnt = 0

    input_ids = torch.tensor([
        vocab[vocab.bos_token],
    ] + vocab[toked]).unsqueeze(0)

    outputs = model.generate(input_ids=input_ids,
                             max_length=50,
                             repetition_penalty=1.2,
                             do_sample=do_sample,
                             num_return_sequences=1)
    print(outputs)
    toked = vocab.to_tokens(outputs[0].squeeze().tolist())
    ret = re.sub(r'(<s>|</s>)', '', ''.join(toked).replace('▁', ' ').strip())

    return ret
