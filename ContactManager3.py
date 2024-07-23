import os 
import re
import json
import bisect
import sys
from tabulate import tabulate

# custom exceptions
class InvalidMobile(Exception):
    pass
class InvalidLandline(Exception):
    pass
class InvalidEmail(Exception):
    pass
class InvalidName(Exception):
    pass

#the class
class Person:
    def __init__(self,name: str=None,mobile: str=None,landline: str=None,email: str=None,addr: str=None) -> None:
        self.name = isname(name)
        self.mobile= ismobile(mobile)
        self.landline= island(landline)
        self.email= isemail(email)
        self.addr= isaddr(addr)
# class methods
# str() and repr() methods for printing the object
    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def editContact(self, **kwargs:str) -> None:
        for key, value in kwargs.items():
            if key == 'name':
                self.name = isname(value)
            elif key == 'mobile':
                self.mobile = ismobile(value)
            elif key == 'landline':
                self.landline = island(value)
            elif key == 'email':
                self.email = isemail(value)
            elif key == 'addr':
                self.addr = isaddr(value)
            else:
                raise IndexError("Invalid Key:")
# end of class


# validation functions pattern check using regex
def isname(val:None|str) -> None|str:
    if val == "" or val == None:
        return None
    pattern = r"^[A-Za-z]+[A-Za-z\s]*[A-Za-z]$"
    s=(re.fullmatch(pattern, val, flags = re.ASCII))
    if s==None:
        raise InvalidName("InvalidName!")
    return val

def ismobile(val:None|str) -> None|str:
    if val == "" or val == None:
        return None
    pattern = r"^[1-9]\d{9}$"
    s=(re.fullmatch(pattern,val, flags = re.ASCII))
    if s==None:
        raise InvalidMobile("InvalidMobile!")
    return val

def island(val:None|str) -> None|str:
    if val == "" or val == None:
        return None
    pattern = r"^[1-9]\d{5,7}$"
    s=(re.fullmatch(pattern,val, flags = re.ASCII))
    if s==None:
        raise InvalidLandline("InvalidLandline!")
    return val

def isemail(val:None|str) -> None|str:
    if val == "" or val == None:
        return None
    pattern = r"^[a-z][a-z0-9]*@[a-z]+\.(com)$"
    s=(re.fullmatch(pattern,val, flags = re.ASCII))
    if s==None:
        raise InvalidEmail("InvalidEmail!")
    return val

def isaddr(val:None|str) -> None|str:
    if val == "" or val == None:
        return None
    return val

def validate(key:str, val:str) -> bool:
    match (key):
        case "name":
            isname(val)
        case "mobile":
            ismobile(val)
        case "landline":
            island(val)
        case "email":
            isemail(val)
        case _:
            raise RuntimeError("Invalid key:")
    return True


# utility functions
def clear() -> None:
    if os.name == "nt":
        os.system('cls')    
    else:
        os.system('clear')
    return None

def exit() -> None:
    clear()
    sys.exit()

# function to convert custom class into json supporting type; dict or list
# argument:  Person() object 
# return type: dict 
def serialize(obj:list|dict|Person) -> list|dict:
    if (isinstance(obj, list) or isinstance(obj, dict)):
        return obj
    else:
        obj = obj.__dict__
        obj['class'] = "Person"
        return obj#dict

# function to convert json object into Person type
# argument: json object or dict
# return type:custom class Person()
def deserialize(obj:list|dict) -> list|dict|Person:
    if isinstance(obj, dict):
        if 'class' in obj:
            return Person(name=obj["name"],mobile=obj["mobile"],landline=obj["landline"],email=obj["email"],addr=obj["addr"])
        else:
            return obj#dict
    return obj

# function returns complete data from json file "contacts.json" 
# checks for the file and contents are present 
# return type: dict with keys as english leters and values: list of contacts of that letter; Person() objects
def read_data() -> dict[str,list[Person]]:
    if os.path.exists("contacts.json") and os.stat("contacts.json").st_size != 0:
        with open("contacts.json", "r") as fp:
            data = json.load(fp, object_hook=deserialize)
    else:
        data = {}
    return data

# function to update json file
# arguments: list of Person() objects
# opens file in write mode 
# while writing, data is converted into json objects(dict)
def dump_data(data:dict[str,list[Person]]):
    with open("contacts.json", "w") as fp:
        json.dump(data, fp, indent = 4, default=serialize)  
        #JSON only supports built-in objects. Calling a function to convert class to dict
    return

#function to sort the dict based on keys() i.e.english letters
def dict_insort(data:dict[str,list[Person]], val:tuple[str,str]) -> dict[str,list[Person]]:
    dict_list = list(data.items())
    bisect.insort(dict_list, val, key = lambda x : x[0])
    return dict(dict_list)

#function to sort list of contacts based on names, starting from same letter
def insert_data(val:Person, contacts:dict[str,list[Person]]) -> dict[str,list[Person]]:
    lst = []
    if (val.name[0].upper() not in contacts):
        lst.append(val)
        tup = (val.name[0].upper(), lst)
        contacts = dict_insort(contacts, tup)
    else:
        bisect.insort(contacts[val.name[0].upper()], val, key = lambda x : x.name)
    return contacts

# function to prompt user for required details
# required fields passed as arguments using *args so that the key can be passed using variable name also
# return type: dict with key as field name and its value input by user
def ask_data(*args:str) -> dict[str,str]:
    args_dict = {}
    for i in args:
        if i == "name":
            args_dict[i] = input("Name:")
        elif i == "mobile":
            args_dict[i] = input("Mobile no.:")
        elif i == "landline":
            args_dict[i] = input("Landline no.:")
        elif i == "email":
            args_dict[i] = input("Mail id(optional):")
        elif i == "addr":
            args_dict[i] = input("Address(optional):")
    return args_dict


# navigation function to prompt user after task completion
def next_page() -> int:
    print("1. Return to home                      2. Exit app")
    while(True):
        try:
            choice = input()
            match (choice):
                case "1":
                    return 0
                case "2":
                    exit()
                case _:
                    raise RuntimeError("Invalid choice:")
        except RuntimeError as err:
            print(err,"Enter choice again.")

# function arguments: 
# 1. a list of 2 elements; name of attribute and its value 
# 2. search domain:- a list of (obj)
# return type: a list of (obj)
def search_contact(search_query:list[str,str], search_list:list[Person]) -> list[Person]:
    search_results = []
    if search_query[0] == "name":
        i = bisect.bisect_left(search_list,search_query[1], key = lambda x : x.name)
        j = bisect.bisect_right(search_list,search_query[1], key = lambda x : x.name)
        search_results.extend(search_list[i:j])
    else:
        for contact in search_list:
            if (search_query[0] == "mobile" and search_query[1] == contact.mobile 
                or search_query[0] == "landline" and search_query[1] == contact.landline 
                or search_query[0] == "email" and  search_query[1].lower() == contact.email.lower()
            ):
                search_results.append(contact)
    return search_results

# data=initial search domain 
def search(data:dict[str, list[Person]]) -> list[Person]:
    while(True):
        try:
            search_query = input("Enter the name, number or email to search as 'key,value': ").split(",")
            if len(search_query) != 2:
                raise ValueError("Invalid input:")
            elif search_query[0] == "name" and search_query[1][0].upper() not in data:
                return []
            elif validate(search_query[0], search_query[1]):
                break
        except RuntimeError as err:
            print(err,"Enter your search query again in 'key,value' format.")
            continue
        except ValueError as err:
            print(err,"Enter your search query again in 'key,value' format.")
            continue
    search_list = []
    if search_query[0] == "name":
        search_list = data[search_query[1][0].upper()]
    else:
        for val in data.values():
            search_list.extend(val)
    search_results = search_contact(search_query, search_list)   
    # a ladder of prompts exceptions to form search_query and search_list and finally call the search_contact() function
    return search_results
    # return type: same as search_contact:- list of (obj) 
    
# driver function for search
# initial search domain is complete data
# results are displayed
def search_data() -> None:
    clear()
    contact_data = read_data()
    people = search(contact_data)
    view(people)
    page = next_page()
    if page == 0:
        return

# function prints contacts in a tabular format
# argument(not compulsory): list of (objects)Person to display 
# else all contacts are displayed
def view(data_lst:list[Person]=None) -> None:
    if data_lst == None:
        data_lst = []
        contact_data = read_data()
        for contact_book in contact_data.values():
            data_lst.extend(contact_book)
    if len(data_lst) > 0:
        table = []
        for index, person in enumerate(data_lst):
            table.append([index + 1, person.name, person.mobile, person.landline, person.email, person.addr])
        headers = ["S.No.", "Name", "Mobile Number", "Landline Number", "Email", "Address"]
        print(tabulate(table, headers, tablefmt="fancy_grid"))
    else:
        print("No contacts found.")
    return

def new() -> None:
    clear()
    print("Enter you data!")
    error = None
    while(True):
        try: 
            if error != None:
                error_dict = ask_data(error) #ask_data(*args) is used to pass variable attribute that has error
                input_dict.update(error_dict)#now the required fields are input successfully
                error = None
            else:
                input_dict = ask_data("name","mobile","landline","email","addr")
            data = Person(**input_dict)
        # error handling and re prompt for input
        except InvalidName as err:
            print(err, "English letters and spaces only.\nEnter again.")
            error = "name"
        except InvalidMobile as err:
            print(err, "Mobile number must 10 contain digits.\nEnter again.")
            error = "mobile"
        except InvalidLandline as err:
            print(err, "Landline number must contain 6-8 digits.\nEnter again.")
            error = "landline"
        except InvalidEmail as err:
            print(err, "Email must be of the form abcde12@gmail.com.\nEnter again.")
            error = "email"
        else:
            break        
    contact_data = read_data()#extracting json data
    contact_data = insert_data(data, contact_data)# adding at correct position
    dump_data(contact_data)#writing the json file with updated data
    page = next_page()
    if page == 0:
        return

def edit() -> None:
    clear()
    contact_data = read_data()
    people=search(contact_data)
    view(people)
    while (True):
        try:
            if len(people) == 0:
                choice = input("Would you like to edit another contact?(y/n)")
                match(choice):
                    case "y":
                        people=search(contact_data)
                        view(people)
                    case "n":
                        page = next_page()
                        if page == 0:
                            return
                    case _:
                        raise RuntimeError("Invalid choice:")
            else:
                index = input("Enter the index of contact to be edited: ")
                if index.isdigit() and int(index) > 0 and int(index) <= len(people):
                    index = int(index)
                    break
                else:
                    raise ValueError("Invalid index: ")
        except ValueError as err:
            print(err, "Enter index again")
            continue
        except RuntimeError as err:
            print(err,"Enter choice again")
            continue
    data={}
    print("Enter details to edit in 'key,value' format\nEnter 'end' to end input")
    cond = "True"
    while (cond != 'end'):
        while(True):
            try:
                detail=input().split(",")
                if detail[0] == 'end':
                    cond = 'end'
                elif len(detail) != 2:
                    raise IndexError("Invalid input:")
                elif detail[0] not in ['name', 'mobile', 'landline', 'email', 'addr']:
                    raise RuntimeError("Invalid key:")
                else:
                    data[detail[0]]=detail[1]
                    people[index-1].editContact(**data)
            except RuntimeError as err:
                print(err,"Enter your search query again in 'key,value' format.")
                continue
            except IndexError as err:
                print(err,"Enter your search query again in 'key,value' format.")
                continue
            except InvalidName as err:
                print(err, "English letters and spaces only.\nEnter again.")
                continue
            except InvalidMobile as err:
                print(err, "Mobile number must 10 contain digits.\nEnter again.")
                continue
            except InvalidLandline as err:
                print(err, "Landline number must contain 6-8 digits.\nEnter again.")
                continue
            except InvalidEmail as err:
                print(err, "Email must be of the form abcde12@gmail.com.\nEnter again.")
                continue
            else:
                break
    dump_data(contact_data)
    page = next_page()
    if page == 0:
        return

def delete() -> None:
    clear()
    contact_data = read_data()
    search_results = search(contact_data)
    view(search_results)
    while True:
        try:
            if len(search_results) == 0:
                choice = input("Would you like to delete another contact?(y/n)")
                match(choice):
                    case "y":
                        search_results=search(contact_data)
                        view(search_results)
                    case "n":
                        page = next_page()
                        if page == 0:
                            return
                    case _:
                        raise RuntimeError("Invalid choice:")
            else:
                choice = input("Enter the S.No. of the contact you want to delete: ")
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(search_results):
                    raise ValueError("Invalid input:")
                break
        except ValueError as err:
            print(err,"Enter the S.No. again.")
            continue
        except RuntimeError as err:
            print(err,"Enter the choice again.")
            continue
    contact = search_results[int(choice) - 1]
    contact_data[contact.name[0].upper()].remove(contact)
    if len(contact_data[contact.name[0].upper()]) == 0:
        del contact_data[contact.name[0].upper()]
    dump_data(contact_data)
    print(f"{contact.name}'s contact deleted successfully.")
    page = next_page()
    if page == 0:
        return


#main
while(True):
    clear()
    print("Welcome to Contact Manager!")
    print("What would you like to do?")
    print("1. Add new contact \n2. Edit a contact \n3. View contacts \n4. Search for a contact \n5. Delete a contact \n6. Exit\n")
    while (True):
        choice = input()
        try:
            match (choice):
                case "1":
                    new()
                case "2":
                    edit()
                case "3":
                    clear()
                    view()
                    page = next_page()
                case "4":
                    search_data()
                case "5":
                    delete()
                case "6":
                    exit()
                case _:
                    raise RuntimeError("Invalid input:")
        except RuntimeError as err:
            print(err,"Enter choice again.")
            continue
        else:
            break