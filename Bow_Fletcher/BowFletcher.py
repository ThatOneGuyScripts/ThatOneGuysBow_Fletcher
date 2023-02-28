import time
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from utilities.geometry import RuneLiteObject
import pyautogui as pag
import model.osrs.Bow_Fletcher.BotSpecImageSearch as imsearch
import utilities.game_launcher as launcher
import pathlib
import model.osrs.Bow_Fletcher.BowFletcher_recipes as Bow_recipes



    
class OSRSBowFletcher(OSRSBot, launcher.Launchable):
    def __init__(self):
        bot_title = "ThatOneGuys Bow Fletcher"
        description = "This bot Fletches unstrung bows."
        super().__init__(bot_title=bot_title, description=description)
        self.what_to_fletch = None
        self.running_time = 1
        self.take_breaks = False
        self.break_length_min = 1
        self.break_length_max = 500
        self.time_between_actions_min =0.8
        self.time_between_actions_max =5
        self.what_to_fletch = None
        self.mouse_speed = "medium"
        self.break_probabilty = 0.13

    def create_options(self):
        self.options_builder.add_dropdown_option("what_to_fletch", "Select Bow to Fletch", Bow_recipes.Bow_names)
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])
        self.options_builder.add_slider_option("break_probabilty", "Chance to take breaks (percent)",1,100)
        self.options_builder.add_slider_option("break_length_min", "How long to take breaks (min) (Seconds)?", 1, 300)
        self.options_builder.add_slider_option("break_length_max", "How long to take breaks (max) (Seconds)?", 2, 300)    
        self.options_builder.add_checkbox_option("mouse_speed", "Mouse Speed (must choose & only select one)",[ "slowest", "slow","medium","fast","fastest"])
        self.options_builder.add_slider_option("time_between_actions_min", "How long to take between actions (min) (MiliSeconds)?", 600,3000)
        self.options_builder.add_slider_option("time_between_actions_max", "How long to take between actions (max) (MiliSeconds)?", 600,3000)
        
                                               
    def save_options(self, options: dict):
        for option in options:
            if  option == "what_to_fletch":
                self.what_to_fletch = options[option]         
            elif option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            elif option == "break_length_min":
                self.break_length_min = options[option]
            elif option == "break_length_max":
                self.break_length_max = (options[option])
            elif option == "mouse_speed":
                self.mouse_speed = options[option]
            elif option == "time_between_actions_min":
                self.time_between_actions_min = options[option]/1000
            elif option == "time_between_actions_max":
                self.time_between_actions_max = options[option]/1000
            elif option == "break_probabilty":
                self.break_probabilty = options[option]/100
                
                
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg(f"We are making {self.what_to_fletch}s")
        self.log_msg("Options set successfully.")
        self.options_set = True


    def launch_game(self):
        settings = pathlib.Path(__file__).parent.joinpath("custom_settings.properties")
        launcher.launch_runelite_with_settings(self, settings)

    def main_loop(self):
        start_time = time.time()
        end_time = self.running_time * 60
        print(self.mouse_speed)
        self.setup()

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            # 5% chance to take a break between tree searches
            if rd.random_chance(probability=self.break_probabilty) and self.take_breaks:
                self.take_break(min_seconds =self.break_length_min, max_seconds=self.break_length_max, fancy=True)   
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()
               
    def bot_loop_main(self):
        print("made it to main loop")
        print(self.what_to_fletch)
        self.withdrawl_ingrediants(self.what_to_fletch)           
        self.close_bank()
        self.Fletch_bows(self.what_to_fletch) 
        self.make_all()      
        self.check_inv(self.what_to_fletch)
        self.find_nearest_bank()
        self.deposit_items()
                         
    def find_nearest_bank(self):
          
        if banks := self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN):
            banks = sorted(banks, key=RuneLiteObject.distance_from_rect_center)
            self.log_msg(f"Bank found")               
            self.mouse.move_to(banks[0].random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            
            
            
        else:
            self.log_msg(f"aay you moron stand near a bank tagged cyan")       
            
    def deposit_items(self):
        Slot_to_click = self.win.inventory_slots[int(rd.fancy_normal_sample(2,27))]
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "deposit.png")
        
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
           
        self.log_msg(f"depositing all items")
        self.mouse.move_to(Slot_to_click.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
        time.sleep(Sleep_time)
    
    def open_up_Fletching_tab(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "deposit.png")
        
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
        Fletching_tab_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "Fletchingtab.png")
        
        if Fletching_tab := imsearch.search_img_in_rect(Fletching_tab_img, self.win.game_view):
            self.log_msg(f"clicking Fletching tab")
            self.mouse.move_to(Fletching_tab.random_point())
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"aaay you idiot there no Fletching tab")
                  
    def open_inventory(self):
        self.log_msg("Selecting inventory...")
        self.mouse.move_to(self.win.cp_tabs[3].random_point(),mouseSpeed=self.mouse_speed[0])
        self.mouse.click()
   
    def set_supplies_amount(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max) 
        withdrawl_all_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "withdrawl_all.png")
        withdrawl_all_clicked_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "withdrawl_all_clicked.png")
        
        if withdrawl_all:= imsearch.search_img_in_rect(withdrawl_all_img, self.win.game_view):
            self.mouse.move_to(withdrawl_all.random_point(),mouseSpeed=self.mouse_speed[0])
            time.sleep(Sleep_time)
            self.mouse.click()
            time.sleep(Sleep_time)
        elif withdrawl_all_clicked := imsearch.search_img_in_rect(withdrawl_all_clicked_img, self.win.game_view):
                 time.sleep(Sleep_time)
        else:
            self.log_msg(f"Could not set withdrawl amount")
            self.log_msg("Finished.")
            self.stop()
          
    def setup(self):
        bow_to_make = f"{self.what_to_fletch}"
        print(bow_to_make)
        
        self.open_inventory()
        self.find_nearest_bank()
        self.open_up_Fletching_tab()
        self.set_supplies_amount()

    def Fletch_bows(self, Fletch_item):
        if Fletch_item in Bow_recipes.Bow_recipes:
            ingredients = Bow_recipes.Bow_recipes[Fletch_item]
            ingredient1, ingredient2,ingredient3 = ingredients
        else:
            self.log_msg(f"No recipe found for {Fletch_item}")
            self.stop()  
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient2)
        Ingrediant_three_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient3)
        
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        if Ingrediant_one := imsearch.search_img_in_rect(Ingrediant_one_img, self.win.control_panel):
            self.mouse.move_to(Ingrediant_one.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"No knife in inventory")
            self.stop()
                
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.control_panel):
            self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
            
    def close_bank(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Close_Bank_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "x.png")
        
        if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
            self.mouse.move_to(Close_bank.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Could not close bank")
            self.stop()
               
    def make_all(self):
        keywords = ["short"]
        Bow_to_make = self.what_to_fletch.lower()
        sleep_time_key = rd.fancy_normal_sample(0.067, 0.084)
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        make_all_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "Make_all.png")  
        make_all_clicked = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", "Make_all_clicked.png")
        
        found_keyword = False
        print(Bow_to_make)
        print(self.what_to_fletch)
        for keyword in keywords:
            if keyword in Bow_to_make:
                found_keyword = True
                break 
        if found_keyword:
            print("keyword found")
            if make_all := imsearch.search_img_in_rect(make_all_clicked, self.win.chat):
                print("make all clicked not found")
                time.sleep(Sleep_time)
                pag.keyDown('2')
                time.sleep(sleep_time_key)
                pag.keyUp('2')
            elif make_all := imsearch.search_img_in_rect(make_all_img, self.win.chat):
                print("make all not clicked not found")
                self.mouse.move_to(make_all.random_point(),mouseSpeed=self.mouse_speed[0])
                self.mouse.click()
                time.sleep(Sleep_time)
                pag.keyDown('2')
                time.sleep(sleep_time_key)
                pag.keyUp('2')
            else:
                self.log_msg(f"Couldn't make all items")
                self.stop()
        else:
            if make_all := imsearch.search_img_in_rect(make_all_clicked, self.win.chat):
                time.sleep(Sleep_time)
                pag.keyDown('3')
                time.sleep(sleep_time_key)
                pag.keyUp('3')
            elif make_all := imsearch.search_img_in_rect(make_all_img, self.win.chat):
                self.mouse.move_to(make_all.random_point(),mouseSpeed=self.mouse_speed[0])
                self.mouse.click()
                time.sleep(Sleep_time)
                pag.keyDown('3')
                time.sleep(sleep_time_key)
                pag.keyUp('3')
            else:
                self.log_msg(f"Couldn't make all items")
                self.stop()
                                    
    def check_inv(self,Fletch_item):
        if Fletch_item in Bow_recipes.Bow_recipes:
            ingredients = Bow_recipes.Bow_recipes[Fletch_item]
            ingredient1, ingredient2,ingredient3 = ingredients
        else:
            self.log_msg(f"No recipe found for {Fletch_item}")
            self.stop()  
        Ingrediant_one_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient1)  
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient2)
        Ingrediant_three_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient3)
        
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0
        finished = False
        while counter < 60 and not finished:
            while True:
                emptyslot27 = imsearch.search_img_in_rect(Ingrediant_three_img, self.win.inventory_slots[27])
                
                if emptyslot27:
                    self.log_msg(f"Finished items")
                    finished = True
                    break
                self.log_msg(f"waiting to finish items")
                counter += 1
                time.sleep(1)
        if finished:
            self.log_msg(f"All items were made")
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"failed to determine if all items were made")
            self.stop()
    
    def withdrawl_ingrediants(self,Fletch_item):
        
        if Fletch_item in Bow_recipes.Bow_recipes:
            ingredients = Bow_recipes.Bow_recipes[Fletch_item]
            ingredient1, ingredient2,ingredient3 = ingredients
            print(ingredient1,ingredient2)
        else:
            self.log_msg(f"No recipe found for {Fletch_item}")
            self.stop()
           
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Ingrediant_two_img = imsearch.BOT_IMAGES.joinpath("Bow_Fletcher_bot", ingredient2)  
        
        if Ingrediant_two := imsearch.search_img_in_rect(Ingrediant_two_img, self.win.game_view):
            self.mouse.move_to(Ingrediant_two.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(Sleep_time)
        else:
            self.log_msg(f"Out of ingredients")
            self.stop()
            