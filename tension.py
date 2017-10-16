"""
Jumayel Islam (c) 2017
"""

import textract
import re
from wnaffect import WNAffect
import nltk
from senti_classifier import senti_classifier


class Tension:

    def __init__(self, corpus):
        self.segments = []
        self.ques = []
        self.ans = []
        self.corpus = textract.process(corpus).decode('utf_8').strip().replace(u'\xa0', u' ')


    def extract_segments(self):

        while True:
            try:
                time1_str = re.search(r'\d{2}:\d{2}:\d{2}', self.corpus).group()
                time1_index = self.corpus.find(time1_str)
                time2_str = re.search(r'\d{2}:\d{2}:\d{2}', self.corpus[time1_index + 8:]).group()
                time2_index = self.corpus.find(time2_str)

                self.segments.append(self.corpus[time1_index + 8:time2_index])
                self.corpus = self.corpus[time2_index:]
            except:
                break

        for seg in self.segments:
            self.extract_ques_ans(seg)


    def extract_ques_ans(self, str):

        end = str.find('Tags')
        tmp_str = str[:end]
        start = tmp_str.rfind('?')

        self.ques.append(str[0:start + 1].strip().replace('\n', ' '))
        self.ans.append(tmp_str[start + 1:end].strip().replace('\n', ' '))


    def extract_polarity_scores(self):

        for question, answer in zip(self.ques, self.ans):
            print(question)
            print(answer)
            pos_score, neg_score = senti_classifier.polarity_scores(nltk.sent_tokenize(answer))
            print(pos_score, neg_score)
            for ls in nltk.sent_tokenize(answer):
                for word in nltk.word_tokenize(ls):
                    emo = wna.get_emotion(word, nltk.pos_tag([word])[0][1])
                    if emo is not None:
                        print(emo)


if __name__ == "__main__":
    wordnet16 = '/home/jumayel/Downloads/wordnet-1.6'
    wndomains32 = '/home/jumayel/Downloads/wn-domains-3.2'
    wna = WNAffect(wordnet16, wndomains32)
    tension = Tension('interview_scripts/interview_sample.doc')
    tension.extract_segments()
    tension.extract_polarity_scores()
