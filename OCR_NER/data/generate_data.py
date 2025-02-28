from names_data import first_names, surnames, districts, wards, Cit_numbers
import random
import json


def generate_data():
    final_output = []
    for i in range(2000):
        tags = ["O", "CIT-NO","GEN","B-PER", "I-PER","YER", "MTH", "DAY", "B-DIST", "B-WARD", "B-NO", "P-DIST", "P-WARD", "P-NO"]

        cit_No = random.choice(Cit_numbers)
        gender = random.choice(["male", "female"])
        f_name = random.choice(first_names)
        l_name = random.choice(surnames)
        DOB_year = random.randint(1970, 2010)
        DOB_month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        DOB_day = random.randint(1, 31)
        Birth_Dis = random.choice(districts)
        Birth_ward = random.choice(wards)
        Birth_no = random.randint(1, 20)
        per_Dis = random.choice(districts)
        per_ward = random.choice(wards)
        per_no = random.randint(1, 20)

        text= (f"details Citizenship Certificate No {cit_No} Sex {gender} Full Name {f_name} {l_name} Date of Birth AD Year{DOB_year} Month {DOB_month} Day {DOB_day} Birth place District {Birth_Dis} VDC {Birth_ward} Ward {Birth_no} Permanent Address District {per_Dis}  Municipality {per_ward} Ward {per_no}")
        tokens = ["details", "Citizenship", "Certificate", "No","{cit_No}","Sex","{gender}","Full","Name","{f_name}","{l_name}","Date","of","Birth","AD",
                "Year{DOB_year}","Month","{DOB_month}","Day","{DOB_day}","Birth","place","District","{Birth_Dis}","VDC","{Birth_ward}","Ward","{Birth_no}",
                "Permanent","Address","District","{per_Dis}","Municipality","{per_ward}","Ward","{per_no}"]
        tokens = [token.format(cit_No=cit_No, gender=gender, f_name=f_name, l_name=l_name, 
                       DOB_year=DOB_year, DOB_month=DOB_month, DOB_day=DOB_day, 
                       Birth_Dis=Birth_Dis, Birth_ward=Birth_ward, Birth_no=Birth_no, 
                       per_Dis=per_Dis, per_ward=per_ward, per_no=per_no) 
          if "{" in token and "}" in token else token 
          for token in tokens]

        ner_tags = [0,0,0,0,1,0,2,0,0,3,4,0,0,0,0,5,0,6,0,7,0,0,0,8,0,9,0,10,0,0,0,11,0,12,0,13]

        output = {
            "tokens": tokens,
            "ner_tags": ner_tags
            }

        final_output.append(output)
        
    return final_output


print("Generating data...")
data = generate_data()

with open("ner_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Data saved to ner_data.json")

