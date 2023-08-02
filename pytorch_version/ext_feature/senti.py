import subprocess
import shlex
import pandas as pd

SentiStrengthLocation = "D:/Project/SentStrength/SentiStrengthCom.jar" #The location of SentiStrength on your computer
SentiStrengthLanguageFolder = "D:/Project/SentStrength/SentStrength_Data/" #The location of the unzipped SentiStrength data files on your computer


def getSentiment(df_text, score='scale'):

    if type(df_text) != pd.Series:
        df_text = pd.Series(df_text)
    df_text = df_text.str.replace('\n', '')
    df_text = df_text.str.replace('\r', '')
    conc_text = '\n'.join(df_text)
    p = subprocess.Popen(shlex.split(
        "java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "' trinary"),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = bytes(conc_text.replace(" ", "+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    stdout_text = stdout_byte.decode("utf-8")
    stdout_text = stdout_text.rstrip().replace("\t", " ")
    stdout_text = stdout_text.replace('\r\n', '')
    senti_score = stdout_text.split(' ')

    senti_score = list(map(float, senti_score))

    senti_score = [int(i) for i in senti_score]
    if score == 'scale':  # Returns from -4 to 4
        senti_score = [sum(senti_score[i:i + 2]) for i in range(0, len(senti_score), 3)]
    elif score == 'binary':  # Return 1 if positive and -1 if negative
        senti_score = [1 if senti_score[i] >= abs(senti_score[i + 1]) else -1 for i in range(0, len(senti_score), 3)]
    elif score == 'trinary':  # Return Positive and Negative Score and Neutral Score
        senti_score = [tuple(senti_score[i:i + 3]) for i in range(0, len(senti_score), 3)]
    elif score == 'dual':  # Return Positive and Negative Score
        senti_score = [tuple(senti_score[i:i + 2]) for i in range(0, len(senti_score), 3)]
    else:
        return "Argument 'score' takes in either 'scale' (between -1 to 1) or 'binary' (two scores, positive and negative rating)"
    return senti_score


def senti_policy(text):
    senti_results = getSentiment(text, score='dual')
    senti_sents = []
    for pos, neg in senti_results:
        if int(neg) * 1.5 + int(pos) < 0:
            senti_sents.append(neg)
        else:
            senti_sents.append(pos)
    return senti_sents


if __name__ == "__main__":
    str_arr = ['improve your standard google', 'where be the ability to save story or even create them from my memory',
               'bad and bad with every update', 'the worst app ever', 'bright white awful and not accessibility friendly for disabled person']
    a = senti_policy(str_arr)
    print(a)
