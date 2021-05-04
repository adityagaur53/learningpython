from peewee import *
import datetime
from datetime import date


db = SqliteDatabase('todo.db')
db.connect()


class todo_db(Model):
    task = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    done = BooleanField(default=False)
    protected = BooleanField(default=False)


    class Meta:
        database = db

class todo_controller:

    def __init__(self):

        self.table = todo_db()
        todo_db.create_table()
        self.selected = 0



    def getall(self):
        all = self.table.select()
        # for item in all:
        #     print(item.task, " time: ", item.timestamp)

        for ind, entry in enumerate(all):

            timestamp = entry.timestamp.strftime('%d/%B/%Y')
            # if timestamp != prev_timestamp:  # same timestamps get printed only once
            print('\n')
            print(timestamp)

            print('=' * len(timestamp))
            if self.selected == ind:
                entry.save()
                print("-"*len(entry.task))
                print(">",entry.task)
                print("-"*len(entry.task))

                self.selectedTimestamp = entry.timestamp
            else:
                entry.save()
                print(entry.task)
            print("Done: ",entry.done)
            print("Protected: ",entry.protected)
        return all
            # prev_timestamp = timestamp


    def previous(self):
        all = self.table.select()
        if self.selected==0:
            self.selected = len(all) -1
        else:
            self.selected-=1
    def next(self):
        all = self.table.select()
        if self.selected>=len(all) - 1:
            self.selected = 0
        else:
            self.selected+=1
    def add_task(self):
        text = input("Enter task: ")
        protect = input("Protect task? (y/n): ")
        if protect == "y":
            self.table.create(task = text, protected = True)
        elif protect == "n":
            self.table.create(task = text, protected = False)
        else:
            print("Invalid Input")

    def modify_menu(self):
        all = self.table.select()
        for ind, entry in enumerate(all):
            if ind == self.selected:
                return True
        return False

    def cleanup(self):

        all = self.table.select() 

        for task in all:

            
            today = datetime.date.today()
            date_now = today.today()
            date_created = date(task.timestamp.year, task.timestamp.month, task.timestamp.day)

            if task.done == True and task.protected == False and (date_now - date_created).days>=7:
                task.delete_instance()

    def quit(self):
        exit()

#second menu
    def modify_task(self):
        all = self.table.select()
        for ind, entry in enumerate(all):
            if ind == self.selected:
                print(entry.task)
                new = input("Enter modified task: ")
                entry.task = new
                entry.save()


    def toggle_done(self):
        all = self.table.select()
        for ind, entry in enumerate(all):
            if ind == self.selected:
                if entry.done == False:
                    entry.done = True
                else:
                    entry.done = False
                entry.save()

    def toggle_protected(self):
        all = self.table.select()
        for ind, entry in enumerate(all):
            if ind == self.selected:
                if entry.protected == False:
                    entry.protected = True
                else:
                    entry.protected = False
                entry.save()
    def erase(self):
        all = self.table.select()
        for ind, entry in enumerate(all):
            if ind == self.selected:
                entry.delete_instance()

    def backtomain(self):
        pass

class todo_menu:
    def __init__(self):
        self.current = None
        self.controller = todo_controller()

    def menu(self):
        while True:

            self.controller.getall()

            print("Previous/Next: p/n \n")
            print("a) Add a new task")
            print("m) Modify selected entry")
            print("c) Cleanup: delete completed, non-protected entries older than a week")
            print("q) Quit")

            self.current  = input("Action: ")

            if self.current == "a":
                self.controller.add_task()

            elif self.current == "p":
                self.controller.previous()

            elif self.current == "n":
                self.controller.next()

            elif self.current == "c":
                self.controller.cleanup()

            elif self.current == "q":
                self.controller.quit()

            elif self.current == "m":
                if self.controller.modify_menu():
                    print("m) Modify task")
                    print("d) Toggle 'DONE'")
                    print("p) Toggle 'protected'")
                    print("e) Erase entry")
                    print("q) Back to Main")

                    self.current = input("Action: ")

                    if self.current == "m":
                        self.controller.modify_task()    #change task to new text

                    elif self.current == "d":
                        self.controller.toggle_done()#toggle done

                    elif self.current == "p":
                        self.controller.toggle_protected()#toggle protected

                    elif self.current == "e":
                        self.controller.erase()#erase entry

                    elif self.current == "q":
                        self.controller.backtomain()#back to main
                else:
                    print("You have to add a task first!")



if __name__ == '__main__':
    menus = todo_menu()
    menus.menu()
