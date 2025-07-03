def match_resume_with_jd(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    matched_words = resume_words.intersection(jd_words)
    if len(jd_words) == 0:
        return 0.0
    return round((len(matched_words) / len(jd_words)) * 100, 2)
