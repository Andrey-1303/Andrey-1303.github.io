import openai
import random

openai.api_key = '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'

category = [['' for _ in range(2)] for _ in range(0)]
category.append(["#top 7", '0'])
category.append(["#top 10", '0'])
category.append(["#top 15", '0'])
category.append(["#top 20", '0'])


# Базовая часть промпта
base_category_prompt = '''What hashtags would you put to this news?
Here are the variants of existing hashtags (you don't have to write them, but if your hashtag is similar to an existing one, write an existing one):
'''

base_text_prompt = '''
Hello. I give you some hashtags, style, mood and another parameters of the text - and you have to write a text

'''

def generate_prompt(prompt,mt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=mt
    )
    return response.choices[0].text.strip()



def generate_name(hashtag):
    prompt = 'Hello. I give you some hashtags, style, mood and another parameters of the text - and you have to write a name of text/news. hashtags(In the answer, I expect only the name of the news and nothing more): \n'+ hashtag
    return(generate_prompt(prompt,100))

def generate_beginning(name_of_text):
    prompt = 'Hello. I will write you the title of the article, and you write the foreword to this article (what is before the article itself, in the answer I expect the text of the beginning of the article and nothing else, without unnecessary words, symbols and without the title itself, etc) Heres the title:\n'+name_of_text    
    return(generate_prompt(prompt,400))

def generate_middle(name_of_text,beginning_of_text):
    prompt = 'Hello. Ill give you the title and the beginning of the article, and its up to you to fill the article with meaning. (the most meat and the main topics, write without water and on topic. write in the format of an entertaining article and as briefly as possible) (In the answer, I expect only the text of the middle of the news, without the title, beginning, unnecessary words, symbols, etc.) Heres the title and text:\n'+name_of_text+'\n'+beginning_of_text
    mid = generate_prompt(prompt,2000)
    return mid

def  generate_end(middle_of_text):
    prompt = 'Hello. Here is the text of my article. Write a beautiful ending for this article\n' + middle_of_text
    return generate_prompt(prompt,400)

def get_category(text):
    global category
    new_category = ['' for _ in range(0)]
    a = ''
    for row in category:
        a = a + row[0] + '\n'
    prompt = base_category_prompt + a + '\n' + 'Here is the title of the news (I expect you to respond in the form of comma-separated words with a space (", ") without the use of extra characters(#,%,$), without additional words, characters and all in one line) \n' + text
    answer = generate_prompt(prompt,300)
    print(prompt,'===',answer)
    for index, value in enumerate(answer.split(", ")):
        new_category.append(value)
    
    for word_to_check in new_category:
        found = False
        for category_row in category:
            if word_to_check == category_row[0]:
                category_row[1] = str(int(category_row[1]) + 1)
                found = True
                break
        if not found:
            category.append([word_to_check, '1'])

    category = sorted(category, key=lambda x: int(x[1]), reverse=True)
    print(category)


def get_random_category():
    global category
    total = sum(int(item[1]) for item in category)
    rand_num = random.uniform(0, total)
    current_sum = 0
    for item in category:
        current_sum += int(item[1])**2
        if rand_num <= current_sum:
            selected_item = item
            break  
    print(selected_item[0]) 
    return selected_item[0]

def generate_raw_text():
    a = ''
    for i in range(random.randint(2,5)):
        a =a + str(get_random_category()) + '\n'
    name_of_text = generate_name(a)
    beggining_of_text = generate_beginning(name_of_text)
    middle_of_text = generate_middle(name_of_text,beggining_of_text)
    end_of_text = generate_end(middle_of_text)
    all_text = beggining_of_text + '\n' + middle_of_text +'\n' + end_of_text
    prompt = ''
    generate_prompt(prompt,20)
    return all_text, name_of_text
 
def generate_average_text():
    raw = generate_raw_text()
    prompt = 'Hello. This is my article. Improve it by keeping the meaning (for example, if the text lists something, leave the same number of enumerations) and increasing the size of the text:\n'+raw[0]
    all_text = generate_prompt(prompt,2048)
    return all_text, raw[1]


def generate_roasted_text():
    average = generate_average_text()
    hint = ''
    prompt = 'Hello. This is my text without edits. Rewrite all my text with the help of this tooltip, as well as add pictures (if you want to add a picture to the text, you need to describe the request for the image very clearly (prompt for dalle, including style, description of the background and background, etc.), all descriptions of the images should be enclosed in four equal signs: ==description of the picture==)(the text of your answer should be at least as large and contain all the same essence and meaning):\n'+hint+'\n and here is the text: \n'+average[0]
    all_text = generate_prompt(prompt,2048)
    return all_text, average[1]
    


get_category('Stay Away: People Share What Interior Design Trends Will Age Poorly')
get_category('Decor on a Dime: 40+ Budget Friendly Home Hacks')
get_category('Create Your Garden Getaway: 25+ Backyard Hacks You Can’t Miss')
get_category('Fix it Fast, Fix it Cheap: 30 Surprising DIY Home Repairs')
get_category('Unlock Your Style Potential Later In Life: 20 Hacks Every Woman Should Know')



print(generate_raw_text())



