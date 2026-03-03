from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal

class QSearchBar(QLineEdit):
    queryUpdated = Signal(list)

    def __init__(self, item_list:list):
        super().__init__()

        self.complete_list = item_list
        self.query_list = item_list

        self.textChanged.connect(self.text_search)
    
    def clear(self):
        super().clear()
        self.text_search()

    def text_search(self):
        # ignore casing
        text = self.text().casefold() # -> lowercase str

        if text:
            # create new list
            query_list = []
            # index every item in existing list
            for format_item_name in self.complete_list:              
                # ignore casing
                item_name = format_item_name.casefold()
                # initialize boolean
                match = False
                # index for every letter in item name
                for item_index in range(len(item_name)):
                    text_index = 0
                    # check if series of letters match beginning at starting letter
                    while item_name[item_index+text_index] == text[text_index]:
                        # if we successfully matched the entire text prompt
                        if text_index == len(text)-1:
                            match = True
                            break

                        elif item_index+text_index == len(item_name)-1:
                            break
                        # go to next letter in text prompt
                        text_index = text_index+1

                    # check if the item matches search
                    if match == True:
                        # add to new list of items
                        query_list = query_list + [format_item_name]
                        break
        
            self.query_list = query_list
        
        else:
            self.query_list = self.complete_list

        self.queryUpdated.emit(self.query_list)