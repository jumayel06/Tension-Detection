# -*- coding: utf-8 -*-
from process import Process
from similarity import Similarity
import glob

if __name__ == "__main__":
    corpora = glob.glob("interview_transcripts/*.docx")
    for corpus in corpora:
        processor = Process(corpus)
        processor.process_html()
        ques_ans = processor.extract_ques_ans()
