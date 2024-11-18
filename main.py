import streamlit as st
from PyKomoran import *
from collections import Counter, defaultdict
import pandas as pd

komoran = Komoran("EXP")

def get_pos_only(analyzed_text):
    analyzed_text_list = analyzed_text.split(' ')
    ret = []
    for part in analyzed_text_list:
        pos = part.split('/')[-1]
        ret.append(pos)
    return ' '.join(ret)

def analyze_text(text):
    ret = defaultdict(str)

    ###########
    res = komoran.get_plain_text(text)
    text_split = res.split(' ')

    ret['vocab_cnt'] = len(text_split)
    ret['analyzed_text'] = res

    pos_seq = get_pos_only(res)
    noun_cnt, verb_cnt = 0, 0
    for pos in pos_seq.split(' '):
        if pos.find('N') == 0:
            noun_cnt += 1
        elif pos.find('VV') == 0:
            verb_cnt += 1

    ret['noun_cnt'] = noun_cnt
    ret['verb_cnt'] = verb_cnt

    ###########
    sentence_list = text.split('.')
    ret['sentence_cnt'] = len(sentence_list)
    sentence_sz = []
    for sent in sentence_list:
        sentence_sz.append(len(sent))
    ret['ASL'] = sum(sentence_sz) / ret['sentence_cnt']

    word_list = text.split(' ')
    word_cnt = len(word_list)
    word_sz = []
    for w in word_list:
        word_sz.append(len(w))
    ret['ASW'] = sum(word_sz) / word_cnt

    # complex word cnt
    complex_word_cnt = 0
    for size in word_sz:
        if size >= 3:
            complex_word_cnt += 1

    ##########
    # FKGL (Flesch-Kincaid Grade Level)
    FKGL = 0.39 * ret['ASL'] + 11.8 * ret['ASW'] - 15.59
    ret['FKGL'] = FKGL

    # GFI (Gunning Fog Index)
    GFI = 0.4 * (word_cnt/ret['sentence_cnt'] + 100*complex_word_cnt/word_cnt)
    ret['GFI'] = GFI

    # Lexical Diversity (어휘 다양성)
    # unique cnt
    unique_cnt = len(set(text_split))
    ret['lexical_diversity'] = unique_cnt * 100 / ret['vocab_cnt']


    return ret


# Streamlit UI
st.title("한국어 텍스트 분석기")
st.subheader("한국어 텍스트의 복잡도를 평가합니다")


# Text input for user
user_text = st.text_area("한국어 텍스트를 입력하세요:", height=200)
st.write('품사표: https://pydocs.komoran.kr/firststep/postypes.html')

if user_text:
    ret = analyze_text(user_text)

    st.write("### 형태소 분석")
    st.write(ret['analyzed_text'])
    st.write('- 단어 갯수: {}'.format(ret['vocab_cnt']))
    st.write('- 명사 갯수: {}'.format(ret['noun_cnt']))
    st.write('- 동사 갯수: {}'.format(ret['verb_cnt']))
    st.write('- 평균 문장 길이: {}'.format(ret['ASL']))
    st.write('- 평균 단어 길이: {}'.format(ret['ASW']))
    st.write('- FKGL (Flesch-Kincaid Grade Level): {}'.format(ret['FKGL']))
    st.write('- GFI (Gunning Fog Index): {}'.format(ret['GFI']))
    st.write('- 어휘 다양성: {} %'.format(ret['lexical_diversity']))
