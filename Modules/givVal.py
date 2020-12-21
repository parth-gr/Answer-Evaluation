import math
import re

import nav_test
import pyrebase
import requests
from fuzzywuzzy import fuzz

import Modules.cosine_similarity as keywordVal
import configurations

# TODO- Accuracy prediction library
'''
e = 1
vg = 2
g = 3
o = 4
p = 5
vp = 6

Grammar:
y = 1
n = 0
'''


def givVal(model_answer, keywords, answer, out_of):
    # KEYWORDS =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # TODO : Enhacnce this thing
    if (len(answer.split())) <= 5:
        return 0
    #
    # count = 0
    # keywords_count = len(keywords)
    # for i in range(keywords_count):
    #     if keywords[i] in answer:
    #         # print (keywords[i])
    #         count = count + 1
    # k = 0
    # if count == keywords_count:
    #     k = 1
    # elif count == (keywords_count - 1):
    #     k = 2
    # elif count == (keywords_count - 2):
    #     k = 3
    # elif count == (keywords_count - 3):
    #     k = 4
    # elif count == (keywords_count - 4):
    #     k = 5
    # elif count == (keywords_count - 5):
    #     k = 6
    k = keywordVal.givKeywordsValue(model_answer, answer)
    # print("checkkkkkk", k)

    # GRAMMAR =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    req = requests.get("https://api.textgears.com/check.php?text=" + answer + "&key=JmcxHCCPZ7jfXLF6")
    no_of_errors = len(req.json()['errors'])

    if no_of_errors > 5 or k == 6:
        g = 0
    else:
        g = 1

    # QST =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # print("fuzz1 ratio: ", fuzz.ratio(model_answer, answer))
    q = math.ceil(fuzz.token_set_ratio(model_answer, answer) * 6 / 100)

    print("Keywords : ", k)
    print("Grammar  : ", g)
    print("QST      : ", q)

    predicted = nav_test.predict(k, g, q)
    # Mathematical model->
    # predicted / 10
    # what?	/ out_of
    result = predicted * out_of / 10
    return result[0]


# model_answer = 'Encapsulation is an object-oriented programming concept that binds together the data and functions that manipulate the data, and that keeps both safe from outside interference and misuse.Data encapsulation led to the important OOP concept of data hiding. If a class does not allow calling code to access internal object data and permits access through methods only, this is a strong form of abstraction or information hiding known as encapsulation. Data encapsulation is a mechanism of bundling the data, and the functions that use them and data abstraction is a mechanism of exposing only the interfaces and hiding the implementation details from the user. Abstraction and encapsulation are complementary concepts: abstraction focuses on the observable behavior of an object. encapsulation focuses upon the implementation that gives rise to this behavior. encapsulation is most often achieved through information hiding, which is the process of hiding all of the secrets of object that do not contribute to its essential characteristics.  Encapsulation is the process of combining data and functions into a single unit called class. In Encapsulation, the data is not accessed directly; it is accessed through the functions present inside the class. In simpler words, attributes of the class are kept private and public getter and setter methods are provided to manipulate these attributes. Thus, encapsulation makes the concept of data hiding possible Abstraction is a process where you show only “relevant” data and “hide” unnecessary details of an object from the user.'

# answer1 = 'It is object oreinted concept related to the data hiding. Abstraction of the program is the encapsulation. It shows the relvant data. It is the mechanism of binding the data, and the function that use them.'

# answer2 = 'Encapsulation is hiding data. It can be visualised as an Abstract view of the program. '

# keywords = ['binds', 'together', 'relevant data', 'data hiding', 'data hiding', 'abstraction', 'combining data']

firebsevar = pyrebase.initialize_app(config=configurations.config)
db = firebsevar.database()

model_answer1 = db.child("model_answers").get().val()[1]['answer']
out_of1 = db.child("model_answers").get().val()[1]['out_of']
keywords1 = db.child("model_answers").get().val()[1]['keywords']
keywords1 = re.findall(r"[a-zA-Z]+", keywords1)

model_answer2 = db.child("model_answers").get().val()[2]['answer']
out_of2 = db.child("model_answers").get().val()[2]['out_of']
keywords2 = db.child("model_answers").get().val()[2]['keywords']
keywords2 = re.findall(r"[a-zA-Z]+", keywords2)

model_answer3 = db.child("model_answers").get().val()[3]['answer']
out_of3 = db.child("model_answers").get().val()[3]['out_of']
keywords3 = db.child("model_answers").get().val()[3]['keywords']
keywords3 = re.findall(r"[a-zA-Z]+", keywords3)

# print(model_answer1)
# print(model_answer2)
# print(model_answer3)

# print(keywords1)
# print(keywords2)
# print(keywords3)


all_answers = db.child("answers").get()

for each_users_answers in all_answers.each():
    # For the first answer ->
    print("\n\n" + each_users_answers.val()['email'])

    answer = each_users_answers.val()['a1']
    result = givVal(model_answer1, keywords1, answer, out_of1)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result1": result})

    # For the Second answer ->
    answer = each_users_answers.val()['a2']
    result = givVal(model_answer2, keywords2, answer, out_of2)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result2": result})

    # For the third answer ->
    answer = each_users_answers.val()['a3']
    result = givVal(model_answer3, keywords3, answer, out_of3)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result3": result})

# out_of = 5
# result = givVal(model_answer, keywords, answer1, out_of)
# print("Final Result : ",result)

# print("fuzzz2 : ",fuzz.token_set_ratio(model_answer,answer2))


# qst1 = answer1.split('Example' or 'eg' or 'example')

# print(qst1[1])
