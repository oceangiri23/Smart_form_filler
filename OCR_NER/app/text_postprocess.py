import re


def interchange_position(text):
    D_target = ["B-DISTRICT","I-DISTRICT"]
    W_target = ["B-WARD","I-WARD"]
    NO_target = ["B-NO","I-NO"]
    D_flag = 0
    W_flag = 0
    NO_flag = 0

    new_words = []

    for data,label in text:
        
        if label in D_target and D_flag == 0:
            label = "B-DISTRICT"
            D_flag = 1

        elif label in D_target and D_flag == 1:
            label = "I-DISTRICT"

        elif label in W_target and W_flag == 0:
            label = "B-WARD"
            W_flag = 1

        elif label in W_target and W_flag == 1:
            label = "I-WARD"

        elif label in NO_target and NO_flag < 2:
            label = "B-NO"
            NO_flag += 1
        
        elif label in NO_target and NO_flag ==2:
            label = "I-NO"
        
        new_words.append((data,label))
        
    return new_words

def prevent_dublicate(text):
    newnew_words = []
    tagss=[]
    for idx , (word, label) in enumerate(text):
        tagss.append(label)
        if label not in ['O']:
            if label in ["B-NO", "I-NO"]:
                    if tagss.count(label) > 2:
                        continue
            elif tagss.count(label) > 1:
                continue
        newnew_words.append((word, label))
    return newnew_words

def extract_num(text):
    match = re.search(r'\d+', text)
    return match.group() if match else None




def get_json(text):
    result = {}
    full_name = []
    citizenship_no = ""
    gender = ""
    year = ""
    month = ""
    day = ""
    B_dist = ""
    B_ward = ""
    B_no = ""
    P_dist = ""
    P_ward = ""
    P_no = ""

    for word, label in text:
        
        if label == "CIT-NUM":
            citizenship_no += word
        elif label == "B-NAME":
            full_name.append(word)
        elif label == "I-NAME":
            full_name.append(word)
        elif label == "SEX":
            gender +=word
        elif label == "YEAR":
            year += word
        elif label == "MONTH":
            month += word
        elif label == "DAY":
            day += word
        elif label == "B-DISTRICT":
            B_dist += word
        elif label == "B-WARD":
            B_ward += word
        elif label == "B-NO":
            B_no += word
        elif label == "I-DISTRICT":
            P_dist += word
        elif label == "I-WARD":
            P_ward += word
        elif label == "I-NO":
            P_no += word

    if citizenship_no:
        citizenship_number = citizenship_no[:2] + "-" + citizenship_no[2:4] + "-" + citizenship_no[4:6] + "-" + citizenship_no[6:]
        result["citizenship_num"] = citizenship_number
    else :
        result["citizenship_num"] = None

    if len(full_name) > 0:
        result["first_name"] = full_name[0]
    else:
        result["first_name"] = None

    if len(full_name) > 1:
        result["last_name"] = full_name[-1]
    else:
        result["last_name"] = None
    if len(gender)>1:
        result["gender"] = gender
    else:
        result["gender"] = None
    if year:
        result["Birth_year"] = year
        result["Birth_year"] = extract_num(result["Birth_year"])
    else:
        result["Birth_year"] = None

    if len(month) >1:
        result["Birth_month"] = month
    else:
        result["Birth_month"] = None
    if day:
        result["Birth_day"] = day
    else:
        result["Birth_day"] = None
    if B_dist:
        result["Birth_district"] = B_dist
    else:
        result["Birth_district"] = None
    if B_ward:
        result["Birth_ward"] = B_ward
    else:
        result["Birth_ward"] = None
    if B_no:
        result["Birth_wardno"] = B_no
        result["Birth_wardno"] = extract_num(result["Birth_wardno"])
    else:
        result["Birth_wardno"] = None
    if P_dist:
        result["Permanent_dist"] = P_dist
    else:
        result["Permanent_dist"] = None
    if P_ward:
        result["Permanent_ward"] = P_ward
    else:
        result["Permanent_ward"] = None
    if P_no:
        result["Permanent_wardno"] = P_no
        result["Permanent_wardno"] = extract_num(result["Permanent_wardno"])
    else:
        result["Permanent_wardno"] = None


    return result


def post_process(text):
    text1 = interchange_position(text)
    text2 = prevent_dublicate(text1)
    text3 = get_json(text2)
    return text3