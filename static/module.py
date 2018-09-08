import time

class Card(object):
    """[summary]
    This class represents a vocabulary card

    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    def __init__(self, front = "", back = ""):
        self.__front = front
        self.__back = back
        self.__timestamp = time.time()
        self.__known = False
    def get_front(self):
        return self.__front
    def get_back(self):
        return self.__back
    def set_front(self, front):
        self.__front = front
    def set_back(self, back):
        self.__back = back
    def reset(self):
        self.__timestamp = time.time()
    def get_timestamp(self):
        return self.__timestamp
    def set_timestamp(self, value):
        self.__timestamp = value
    def set_known(self, flag):
        self.__known = flag
    def get_known(self):
        return self.__known

class Compartment(object):
    def __init__(self, i):
        self.__cards = []
        self.id = i
        self.__iter = iter(self.__cards)
        self.C = 1.1
    def add_card(self, cd):
        assert isinstance(cd, Card), "Obj must be Card"
        for c in self.__cards:
            if c.get_front() == cd.get_front() and c.get_back() == cd.get_back():
                raise Exception("add_card: Duplicate!")
        self.__cards.append(cd)
    def remove_card(self, cd):
        assert isinstance(cd, Card), "Obj must be Card"
        for c in self.__cards:
            if c.get_front() == cd.get_front() and c.get_back() == cd.get_back():
                self.__cards.remove(c)
                return
        raise Exception("remove_card : The card don't exists")
    def get_cards(self):
        return self.__cards
    def get_card(self, front, back):
        for cd in self.__cards:
            if cd.get_front() == front and cd.get_back() == back:
                return cd
        return None
    def size(self):
        return len(self.__cards)
    def next_card(self):
        try:
            return self.__iter.next()
        except:
            self.__iter = iter(self.__cards)
            return self.__iter.next()
    def reset(self):
        self.__cards = []

class FillingBox(object):
    def __init__(self):
        self.__compartments = []
        for i in range(5):
            self.__compartments.append(Compartment(i+1))
        self.__selected = 0
        self.__MAIN = 0
    def add_card(self,cd):
        self.__compartments[self.__MAIN].add_card(cd)
    def remove(self,i, cd):
        assert i >= 0 and i < 5
        self.__compartments[i].remove_card(cd)
    def select(self, i):
        assert i >= 0 and i < len(self.__compartments)
        self.__selected = i
    def __str__(self):
        ans = ""
        for i in range(5):
            ans += "\n\tBox {0}\n\n".format(i)
            for cd in self.__compartments[i].get_cards():
                ans += "{0}, {1} \n".format(cd.get_front(), cd.get_back())
        return ans
    def get_compartments(self):
        return self.__compartments
    def is_empty(self):
        for com in self.__compartments:
            if com.size() > 0:
                return False
        return True
    def learn(self):
        cd = self.__compartments[self.__selected].next_card()
        assert cd
        # counter = 0
        # while (time.time() - cd.get_timestamp()) < (86400 * (self.__selected + 1)):
        #     cd = self.__compartments[self.__selected].next_card()
        #     counter += 1
        #     if counter > self.__compartments[self.__selected].size():
        #         return None
        return cd
    def is_known(self, cd):
        cd.reset()
        cd.set_known(False)
        self.__compartments[self.__selected + 1].get_cards().append(cd)
        self.__compartments[self.__selected].get_cards().remove(cd)
    def is_unknown(self, cd):
        cd.reset()
        cd.set_known(False)
    def reset(self):
        for com in self.__compartments:
            com.reset()
    def save(self, path):
        file = open(path,"w")
        content = ""

        for i in range(5):
            for cd in self.__compartments[i].get_cards():
                content += "{0};{1};{2};{3}\n".format(i, cd.get_front(), cd.get_back(), cd.get_timestamp())
        
        file.write(content)

        file.close()
    def load(self, path):
        self.reset()
        words = []
        file = open(path)
        for line in file:
            words = line.split(";")
            cd = Card(words[1], words[2])
            cd.set_timestamp(float(words[3]))
            self.__compartments[int(words[0])].add_card(cd)
        file.close()
    def create_CSV(self):
        content = ""

        for i in range(5):
            for cd in self.__compartments[i].get_cards():
                content += "{0};{1};{2};{3}\n".format(i, cd.get_front(), cd.get_back(), cd.get_timestamp())
        
        return content

    
    
