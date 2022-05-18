
from sys import exit
from random import randint
from timeit import default_timer as timer


coordinates = ['N','S','E','W']


class Room():

      def __init__(self,name):
          self.name = name
          self.doors = []
          self.items = {}       # the dict will have the name of the item as key, and the itemobject as value
          self.hidden_items = {}

class Item():                   # Stationary item
        def __init__(self,name):
            self.name = name
            self.ismovable = False

class Movable_item(Item):
        def __init__(self,name):
            super().__init__(name)
            self.ismovable = True


class Usable_item(Item):
        def __init__(self,name,action):
            super().__init__(name)
            self.ismovable = True
            self.action = action


class Game_round():

        def __init__(self,rooms,doors,items,start):
            self.rooms = {}
            self.backpack = {'water': Movable_item('water'),'flashlight': Movable_item('flashlight')}      # necklace:
            self.win = False
            for room in rooms:
                self.rooms[room] = Room(room)
            for door in doors:
                self.rooms[door[2]].doors.append([door[0][0],door[1],door[3]])
                self.rooms[door[3]].doors.append([door[0][2],door[1],door[2]])
            for item in items:
                if item[2] == "STATIONARY":
                    new_item = Item(item[0])
                    self.rooms[item[1]].items[item[0]] = new_item
                if item[2] == "MOVE":
                    new_item = Movable_item(item[0])
                    # if add MOVE-object, they need to have a string after MOVE in config-file
                    if item[3] == 'hidden':
                        self.rooms[item[1]].hidden_items[item[0]] = new_item
                    else:
                        self.rooms[item[1]].items[item[0]] = new_item
                if item[2] == "USE":
                    new_item = Usable_item(item[0],item[3])
                    self.rooms[item[1]].items[item[0]] = new_item


            self.current = self.rooms[start[0]]

            print()
            print("Welcome to the game!")
            print('You are an expert jewelry thief, and you have found the residence ')
            print('of one of the foremost Victorian jewelry collectors in New Yorks\'s Upper ')
            print('East side. He is away on vacation with his wife. You must find the necklace that')
            print('the collector recently bought at auction for his wife somewhere in the home. ')
            print('You will teleport out of the house after you grab the necklace.')
            print()
            print('Good luck!')
            print()

            valid_level = False
            while valid_level == False:
              print('Would you like to play the game with maximum or minimum difficulty?')
              print('Options: min, max')
              answer = input('> ')
              if len(answer) < 1:
                  answer = 'incorrect'
              answer = answer.split()[0]
              self.level = 'max'
              if answer == 'min':
                self.level = 'min'
                print('You have picked the minimum level of difficulty.')
                valid_level = True
              elif answer == 'max':
                print('You have picked the maximum level of difficulty.')
                valid_level = True
                print()
                print('There is a problem, you have set off the alarm as you entered the house!')
                print('It has automatically called the police. ')
                print('They will be here in 3 minutes.')
                print('That is the maximum amount of time you have to find the necklace in the house and take it.')
              else:
                print("This is not a valid command. Type either 'min' or 'max'.")
                print()
            self.start_time = timer()
            self.make_action('show')


        def run_game(self, playing):
            if self.level == 'max':
              now = timer()
              passed_time = now - self.start_time
              print('Time passed:',int(passed_time),'seconds')
            else:
              passed_time = 0
            if playing == True and self.win:
                print()
                print ('YOU HAVE WON THE GAME')
                print()
            elif playing == True and passed_time < 180:    #
                self.status = self.make_action(input('> '))
                self.run_game(self.status)

            else:
                print()
                print ('GAME OVER')
                print()

        def make_action(self, command):
            global coordinates
            command = command.split()
            if len(command) == 0:
                return True

            if command[0] == 'quit':
                return False

            elif command[0] == 'go':
                if len(command) < 2:
                    print(f'go-command requires an argument.')
                    return True
                available_doors = [door[0] for door in self.current.doors]
                if command[1] in available_doors:
                    which_door = available_doors.index(command[1])
                    if self.current.doors[which_door][1] == 'open':
                        self.current = self.rooms[self.current.doors[which_door][2]]
                        self.make_action('show')
                    elif self.current.doors[which_door][1] == 'closed':
                        print ('The door is closed. You have to open the door.')
                    elif self.current.doors[which_door][1] == 'locked':
                        print('The door is locked. You can unlock it if you have a key.')
                    return True
                else:
                    print('You cannot move in that direction.')
                return True

            elif command[0] == 'open':
                if len(command) < 2:
                    print(f'open-command requires an argument.')
                    return True
                available_doors = [door[0] for door in self.current.doors]
                if command[1] in available_doors:
                    which_door = available_doors.index(command[1])
                    if self.current.doors[which_door][1] == 'closed':
                        self.current.doors[which_door][1] = 'open'
                # Changing the door for the adjacent room as well
                        name_adjacent = self.current.doors[which_door][2]
                        next_available_doors = [door[2] for door in self.rooms[name_adjacent].doors]
                        print ('You have opened the door.')
                        change_door = next_available_doors.index(self.current.name)
                        self.rooms[name_adjacent].doors[change_door][1] = 'open'
                    elif self.current.doors[which_door][1] == 'locked':
                        print('You cannot open this door unless you have a key.')
                        print('Try the unlock-command.')
                elif command[1] in coordinates:
                    print('There is no door in that direction.')
                elif command[1] in self.current.items:
                    if isinstance(self.current.items[command[1]],Usable_item):
                        if self.current.items[command[1]].action == 'open':
                            self.current.items.update(self.current.hidden_items)
                            print(f'You have opened the {command[1]}.')
                    else:
                        print('This item is not usable.')
                else:
                    print(f'There is no such item {command[1]} in the room.')
                return True

            elif command[0] == 'release':
                if len(command) < 2:
                    print ('You have to state what item to release.')
                    return True
                item_to_drop = command[1]
                if item_to_drop in self.backpack:
                    self.current.items[item_to_drop] = self.backpack[item_to_drop]
                    self.backpack.pop(item_to_drop)
                    print (f'You have released {item_to_drop}.')
                else:
                     print(f'{item_to_drop} is not in your backpack.')
                return True

            elif command[0] == 'show':
                print()
                print (f'You are in the {self.current.name}.')
                string_of_doors: ([door[0] for door in self.current.doors])
                print (f"There are doors towards {', '.join([door[0] for door in self.current.doors])}.")
                if len(self.current.items) > 0:
                    print('Here are the following items:')
                    for item in self.current.items:
                        print (self.current.items[item].name)
                print()
                return True

            elif command[0] == 'take':
                #command_list = command.split()
                if len(command) < 2:
                    print(f'take-command requires an argument.')
                    return True
                if command[1] in self.current.items:
                    if self.current.items[command[1]].ismovable:
                        self.backpack[command[1]] = self.current.items[command[1]]
                        self.current.items.pop(command[1])
                        print(f'You have taken the following item: {command[1]}.')
                        if command[1] == 'necklace':
                          self.win = True
                          return True
                        else:
                          pass
                    else:
                        print (f'{command[1]} is not movable.')
                else:
                    print(f'{command[1]} is not in the room.')
                return True

            elif command[0] == 'holding':
                for item in self.backpack:
                    print(item)
                return True

            elif command[0] == 'commands':
                    commands_list = ['These are the available commands:','','go DIR','take ITEM',\
                    'release ITEM','holding','open DIR','show','commands','open ITEM','unlock DIR' ,'quit']
                    for com in commands_list:
                        print(com)
                    return True

            elif command[0] == 'unlock':
                if len(command) < 2:
                    print(f'unlock-command requires an argument.')
                    return True
                if 'key' in self.backpack:
                    available_doors = [door[0] for door in self.current.doors]
                    if command[1] in available_doors:
                        which_door = available_doors.index(command[1])
                        if self.current.doors[which_door][1] == 'locked':
                            self.current.doors[which_door][1] = 'closed'
                    # Changing the door for the adjacent room as well
                            name_adjacent = self.current.doors[which_door][2]
                            next_available_doors = [door[2] for door in self.rooms[name_adjacent].doors]
                            change_door = next_available_doors.index(self.current.name)
                            self.rooms[name_adjacent].doors[change_door][1] = 'open'
                            print('You have unlocked the door.')
                        else:
                            print('The door is not locked.')
                    else:
                        print('There is no door in that direction.')

                else:
                    print(f'You do not have the key to unlock any locked doors.')
                return True

            print('That is not an intelligible command. Try again.')
            return True


def read_config(filename):
  rooms = []
  doors = []
  items = []
  start = []
  with open(filename, "r") as infile:
      for line in infile:
        if line[:4] == 'room':
          line = line.split()
          rooms.append(line[1])
        if line[:4] == 'door':
          line = line.split()
          doors.append(line[1:])
        if line[:4] == 'item':
          line = line.split()
          items.append(line[1:])
        if line[:5] == 'start':
          line = line.split()
          start.append(line[1])

  return rooms,doors,items,start


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
      print ('Please provide a configuration file after .py file. ')
  else:
      config_file = sys.argv[1]
      rooms,doors,items,start = read_config(config_file)
      game_round_obj = Game_round(rooms,doors,items,start)
      game_round_obj.run_game(True)

# Lägg till:
# rumdeskription i hallen
