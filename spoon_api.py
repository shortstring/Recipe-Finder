#Ashton Smith
#Mini-capstone project
#spoon_api.py
#this file is used to make requests to the spoonacular api.
import requests
import os
from dotenv import load_dotenv


#this function is takes an argument (1-4) and returns the key value (category)
def category(option):
    cat_dict = {
    1:'recipes',
    2:'ingredients',
    3:'menuItems',
    4:'products'
    }
    return cat_dict[option] 



#this class is used to prompt the user for what they want to search for (query)
def prompt_query():
    return input("What do you want to search for?\n")



#this class is used to make requests to spoon api
class spoon:
    def __init__(self,category,query) -> None:
        self.category = category
        self.query = query



    #this function is used to make a request to spoon
    def get_data(self):
        url_dict = {
            'recipes' : 'recipes/complexSearch?',
            'ingredients':'food/ingredients/search?',
            'menuItems': 'food/menuItems/search?',
            'products': 'food/products/search?'
        }
        load_dotenv()
        TOKEN = os.getenv('TOKEN')
        url = f'https://api.spoonacular.com/{url_dict[self.category]}query={self.query}&apiKey={TOKEN}'
        response = requests.get(url)
        data = response.json()
        print(data)
        # self.data_printer(data)
        return data



    #this function seperates the data into steps and ingredients
    def data_printer(self,my_data):
        if 'code' in my_data and my_data['code']: #401 unauthorized
            print('error ' + my_data['code'])
            return my_data['code']

        print('Matches found: ' + str(my_data['totalResults']))
        
        #loop through results (list of recipes)    
        for i in my_data['results']:
            # curr_image = i['image']
           
            curr_id = i['id'] #recipe id

            #request full recipe using id
            load_dotenv()
            TOKEN = os.getenv('TOKEN') #api key
            cur_url = f'https://api.spoonacular.com/recipes/{curr_id}/information?includeNutrition=true&apiKey={TOKEN}'
            response = requests.get(cur_url)
            data = response.json()
            
            print(data['title'])
            #print ingredients
            for i in data['extendedIngredients']:
                print(i['originalString'])
        
            #print instructions
            for i in data['analyzedInstructions']:
                for j in i['steps']:
                    print ('\nStep ' + str(j['number']) + ': ')
                    print (j['step'] + '\n')
            
            #next recipe or exit
            if input('Enter x to exit') == 'x':
                break



# #this function is used to test the spoon_api class
# def test_func():

#     cat = category(1)
#     query = prompt_query()
#     my_spoon = spoon(cat, query)
#     my_data = my_spoon.get_data()
#     my_spoon.data_printer(my_data)
