from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import requests
import os
from dotenv import load_dotenv
import spoon_api



#this class contains all tkinter functions
class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        img = tk.Image("photo", file="my_icon.png")
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.current = 0 #current recipe from current complex search 0-9
        self.my_search = None #search results - could be an error
        self.title("Recipe Finder")
        self.configure(bg='#79baa9')
        self.minsize(500,400)
        self.grid_columnconfigure(0, weight=1)#used for tk.obj.grid()
        self.ingredients = '' #string of ingredients to be printed to the window
        self.favorites = None #list of dicts [{'name':'recipe name','id':'9939393'},{'name':'recipe name','id':'9939393'}]
        self.blocked = None #blocked/ignored recipes (recipe will be skipped)
        self.state = 0 #are there any widgets? 1 = yes 0 = no
        self.load_favorite()#load favorite combo
        self.load_blocked()#load radio combo
        self.favorite_recipes = StringVar() #combo box options
        self.blocked_recipes = StringVar() #combo box options
        self.search_window_builder()
       

    #creates the widgets for the search menu (first screen)
    def search_window_builder(self):
        self.favorites = None
        self.blocked = None
        self.load_favorite()
        self.load_blocked()
        self.label_search = tk.Label(self, text = 'Enter a search term: ')
        self.label_search.grid(pady = (20,1))
        
        self.box_search = tk.Text(width= 10, height= 1)
        self.box_search.grid(pady= (20,2))
        
        self.button_search = tk.Button(self, text = 'search', command = self.click_search)
        self.button_search.grid(pady= (20,3))

        self.combobox_favorites = ttk.Combobox(self, width = 20, textvariable = self.favorite_recipes)
        for i in self.favorites:
            self.combobox_favorites['values'] = (*self.combobox_favorites['values'],str(i['name']))
        self.combobox_favorites.grid(pady = (20,4))

        self.button_favorite = tk.Button(self, text = 'go favorite', command = self.click_favorite)
        self.button_favorite.grid(pady = (20,5))
        
        self.combobox_blocked = ttk.Combobox(self, width = 20, textvariable = self.blocked_recipes)
        for i in self.blocked:
            self.combobox_blocked['values'] = (*self.combobox_blocked['values'],str(i['name']))
        self.combobox_blocked.grid(pady = (20,6))

        self.button_blocked = tk.Button(self, text = 'blocked', command = self.click_block)
        self.button_blocked.grid(pady = (20,7))
        
        self.state += 1



    #This function opens an image from the api, then it creates the image and puts it in a tk label object 
    def pack_img(self, img_name):   
        img = Image.open(requests.get(img_name, stream= True).raw)#open image associated with result
        img = img.resize((250, 250))
        tkimage = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self, image=tkimage)
        self.img_label.image = tkimage
        self.img_label.grid(pady= (5,5))



    #this function is used to remove a blocked item
    def click_block(self):
        print('block clicked')
        


    #this function loads data from a .csv file 
    def click_favorite(self):
        recipe_selected = self.combobox_favorites.get()
        recipe_id = None
        self.clear_search_window()
        for i in self.favorites:
            print(i)
            if recipe_selected == i['name']:
                recipe_id = i['id']
                break
        self.request_id(recipe_id)



    #makes a request given an id (arg), then populates variables and calls function to create widgets
    def request_id(self,curr_id):
            load_dotenv()
            TOKEN = os.getenv('TOKEN') #api key
            cur_url = f'https://api.spoonacular.com/recipes/{curr_id}/information?includeNutrition=true&apiKey={TOKEN}'
            response = requests.get(cur_url)
            data = response.json()
            self.curr_id = curr_id
            self.my_title = data['title']
            self.curr_image = data['image']

            #print ingredients
            z = 0
            self.ingredients = ''
            for i in data['extendedIngredients']:
                if z < 2:
                    self.ingredients += i['originalString'] + ', '
                else:
                    self.ingredients += i['originalString'] + '\n'
                    z -= 3 
                z += 1
                
            #print instructions
            self.my_steps = ''
            for i in data['analyzedInstructions']:
                for j in i['steps']:
                    if len(j['step']) > 50:
                        v = j['step'].split('.')
                        self.my_steps += 'Step ' + str(j['number']) +': '
                        for word in v:
                            self.my_steps += word + '\n'
                    else:
                        self.my_steps += 'Step ' + str(j['number']) +': ' + str(j['step']) +'\n'

            self.fill_window()



    #this function is used to load favorite recipes from a .csv
    def load_favorite(self):
        with open('favorites.csv') as f:
            lines = f.read().split('\n')
        favorites = []
        header = lines[0].split(',')
        for i in range(1, len(lines)):
            row = lines[i].split(',')
            contact = dict(zip(header, row))
            favorites.append(contact)
        self.favorites = favorites



    #this function loads blocked names and ids from n external csv file
    def load_blocked(self):
        with open('blocked.csv') as f:
            lines = f.read().split('\n')
        blocked = []
        header = lines[0].split(',')
        for i in range(1, len(lines)):
            row = lines[i].split(',')
            contact = dict(zip(header, row))
            blocked.append(contact)
        self.blocked = blocked



    #this function is used to block a recipe
    def block_recipe(self):
        with open('blocked.csv','a') as fd:
            fd.write('\n' + str(self.my_title) + ',' + str(self.curr_id))
        print('recipe blocked')



    #this function is used to save a recipe name and id
    def save_recipe(self):
        with open('favorites.csv','a') as fd:
            fd.write('\n' + str(self.my_title) + ',' + str(self.curr_id))
        print('recipe saved')



    #clears window with destroy().. the recipe window with the image
    def screen_clear(self):
        self.label_title.destroy()
        self.img_label.destroy()
        self.label_steps.destroy()
        self.label_ingredients.destroy()
        self.button_next.destroy()
        self.button_block.destroy()
        self.button_save.destroy()
        self.button_newsearch.destroy()
        self.state -= 1 # state = 0



    #this function is used to clear the window (initial window with search and favorites)
    def clear_search_window(self):
        self.label_search.destroy()
        self.box_search.destroy()
        self.button_search.destroy()
        self.button_favorite.destroy()
        self.combobox_favorites.destroy()
        self.combobox_blocked.destroy()
        self.button_blocked.destroy()
        self.state -= 1 # state = 0



    #called when next button is clicked (button on recipe screen)
    def next_button(self):
        self.screen_clear()
        self.data_wrapper()

  

    #this function is called when the search button is clicked. It clears the window and then calls the search function. 
    # Recipes are displayed one at a time
    def click_search(self):
        self.current = 0
        name = StringVar(self)
        name = self.box_search.get('1.0', 'end-1c')
        self.clear_search_window()
        cat = spoon_api.category(1)
        my_spoon = spoon_api.spoon(cat, name)
        self.my_search = my_spoon.get_data()
        self.data_wrapper()



    #fills window with recipe widgets
    def fill_window(self):
        if self.state == 1:
            self.screen_clear()
        self.button_next = tk.Button(self, text = 'Next', command = self.next_button)
        self.button_next.grid( pady= (5,0))
        
        self.button_block = tk.Button(self, text= 'Block Recipe', command = self.block_recipe)
        self.button_block.grid( pady= (5,0))

        self.button_save = tk.Button(self, text= 'Save Recipe', command = self.save_recipe)
        self.button_save.grid( pady= (5,0))

        self.button_newsearch = tk.Button(self,text = 'New Search', command  = self.new_search_button)
        self.button_newsearch.grid(pady= (5,4))
        
        font_tuple = ("Comic Sans MS", 20, "bold")
        self.label_title = tk.Label(self, text = self.my_title)
        self.label_title.grid(pady= (5,5), padx= (5,5))
        self.label_title.configure(font=font_tuple)
        self.pack_img(self.curr_image)
        
        font_tuple = ("Comic Sans MS", 8)
        self.label_ingredients = tk.Label(self, text = self.ingredients)
        self.label_ingredients.configure(font= font_tuple,justify='left')
        self.label_ingredients.grid(pady= (10,10),padx=(10,10))

        self.label_steps = tk.Label(self, text = self.my_steps)
        self.label_steps.grid(pady= (10,10), padx=(10,10))
        self.label_steps.configure(font= font_tuple)
        
        self.state += 1



    #this function will bring the user back to the search screen
    def new_search_button(self):
        self.screen_clear()
        self.search_window_builder()



    #this function is used to check for error codes and then it will call the function to perform the api request
    def data_wrapper(self):
        #if no search
        if self.my_search == None:
            self.search_window_builder()
            return 0
        #error code
        if 'code' in self.my_search and self.my_search['code'] == 401: #401 unauthorized
            print('error 401')
            return 0
        print('Matches found: ' + str(self.my_search['totalResults']))
        #loop through results (list of recipes)
        x = 0   
        for i in self.my_search['results']:
            if(self.current == x):
                self.data_printer(i)
                return 0
            x += 1
        return 1
        #######################
        #may need to make a second request and pass an offset -- current result only holds (10?) results



    #this function makes a request to the api - fills the variables and finally calls a function to build the window
    def data_printer(self,my_data):
        self.current += 1
        self.curr_image = my_data['image'] #recipe image ex: 'image':'https://spoonacular.com/recipeImages/64763-312x231.jpg
        self.curr_id = my_data['id'] #recipe id
        for i in self.blocked:
            if int(i['id']) == int(self.curr_id):
                print('current recipe is blocked.. skipping it')
                self.data_wrapper()
                return 0
        #request full recipe using id
        load_dotenv()
        TOKEN = os.getenv('TOKEN') #api key
        cur_url = f'https://api.spoonacular.com/recipes/{self.curr_id}/information?includeNutrition=true&apiKey={TOKEN}'
        response = requests.get(cur_url)
        data = response.json()
        self.my_title = my_data['title']
        #print ingredients
        z = 0
        self.ingredients = ''
        for i in data['extendedIngredients']:
            if z < 2:
                self.ingredients += i['originalString'] + ', '
            else:
                self.ingredients += i['originalString'] + '\n'
                z -= 3 
            z += 1
        #print instructions
        self.my_steps = ''
        for i in data['analyzedInstructions']:
            for j in i['steps']:
                if len(j['step']) > 50:
                    v = j['step'].split('.')
                    self.my_steps += 'Step ' + str(j['number']) +': '
                    for word in v:
                        self.my_steps += word + '\n'
                else:
                    self.my_steps += 'Step ' + str(j['number']) +': ' + str(j['step']) +'\n'
        self.fill_window()



#
def main():
    window = Window()
    window.mainloop()



main()