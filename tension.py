"""
Jumayel Islam (c) 2017
"""

import textract
import re
import nltk
import glob


class Tension:

    def __init__(self, corpus):
        self.segments = []
        self.ques = []
        self.ans = []
        self.interviewer = ""
        self.interviewee = ""
        self.corpus = textract.process(corpus).decode('utf_8').strip().replace(u'\xa0', u' ')

    def extract_segments(self):
        initial_time = re.search(r'\d{2}:\d{2}:\d{2}', self.corpus).group()
        initial_time_index = self.corpus.find(initial_time)
        self.corpus = self.corpus[initial_time_index + 8:]
        self.corpus = self.corpus.replace('\n', ' ')
        words = self.corpus.split(' ')
        candidates = []
        for word in words:
            if ":" in word:
                candidates.append(word)
        fdist = nltk.FreqDist(candidates)
        candidate1 = fdist.most_common(2)[0][0].replace(':','')
        candidate2 = fdist.most_common(2)[1][0].replace(':','')

        if self.corpus.find(candidate1) < self.corpus.find(candidate2):
            self.interviewer = candidate1
            self.interviewee = candidate2
        else:
            self.interviewer = candidate2
            self.interviewee = candidate1

        while True:
            indices = [s.start() for s in re.finditer(self.interviewer+":", self.corpus)]
            if len(indices) < 2:
                self.segments.append(self.corpus[indices[0]:])
                break
            self.segments.append(self.corpus[indices[0]:indices[1]])
            self.corpus = self.corpus[indices[1]:]

    def extract_ques_ans(self):
        for segment in self.segments:
            self.ques.append(segment[segment.find(self.interviewer)+len(self.interviewer)+1:
                             segment.find(self.interviewee)].strip())
            self.ans.append(segment[segment.find(self.interviewee) + len(self.interviewee) + 1:].strip())

if __name__ == "__main__":
    corpora = glob.glob("interview_transcripts/*.docx")
    for corpus in corpora:
        tension = Tension(corpus)
        tension.extract_segments()
        tension.extract_ques_ans()