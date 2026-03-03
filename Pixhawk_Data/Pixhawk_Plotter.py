import numpy as np
import matplotlib.pyplot as plt
from pyulog import ULog
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot,Signal

def title_formatter(title:str):
    title = title.replace("_"," ")
    title = title.title()
    return title

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

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.axis_font_size = 15
        self.tick_mark_size = 10
        self.title_font_size = 20

        self.setWindowTitle("Plot Creator")
        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        self.file_path_lbl = QLabel("Log File Path:")
        layout.addWidget(self.file_path_lbl)

        self.file_path_btn = QPushButton("Select Log File")
        self.file_path_btn.clicked.connect(self.select_log_file)
        layout.addWidget(self.file_path_btn)

        self.dataset_label = QLabel("Available Datasets:")
        layout.addWidget(self.dataset_label)

        self.dataset_names = []
        self.dataset_search = QSearchBar(item_list=self.dataset_names)
        self.dataset_search.queryUpdated.connect(self.search_datasets)
        layout.addWidget(self.dataset_search)

        self.dataset_select = QListWidget()
        self.dataset_select.itemClicked.connect(self.select_dataset)
        layout.addWidget(self.dataset_select)

        self.data_key_label = QLabel("Available Parameters:")
        layout.addWidget(self.data_key_label)

        self.dataset_keys = None
        self.data_key_select = QListWidget()
        self.data_key_select.itemClicked.connect(self.select_data_key)
        layout.addWidget(self.data_key_select)

        x_axis_group = QGroupBox("Select x-axis")
        x_axis_layout = QHBoxLayout(x_axis_group)

        self.x_axis_select = QButtonGroup(x_axis_group)
        self.x_axis_select.setExclusive(True)

        self.ToF_btn = QRadioButton("Time of Flight")
        self.armed_time_btn = QRadioButton("Time Armed")
        self.num_samples_btn = QRadioButton("Number of Samples")

        btn_ID = 0
        for btn in (self.num_samples_btn,self.ToF_btn,self.armed_time_btn):
            x_axis_layout.addWidget(btn)
            self.x_axis_select.addButton(btn,btn_ID)
            btn_ID += 1

        self.num_samples_btn.setChecked(True)

        layout.addWidget(x_axis_group)


        text_override_group = QGroupBox("Override Text Size")
        text_override_layout = QHBoxLayout(text_override_group)

        self.title_font_size_label = QLabel("title:")
        text_override_layout.addWidget(self.title_font_size_label)

        self.title_font_size_entry = QLineEdit()
        self.title_font_size_entry.setText(str(self.title_font_size))
        text_override_layout.addWidget(self.title_font_size_entry)

        self.axis_font_size_label = QLabel("axis:")
        text_override_layout.addWidget(self.axis_font_size_label)

        self.axis_font_size_entry = QLineEdit()
        self.axis_font_size_entry.setText(str(self.axis_font_size))
        text_override_layout.addWidget(self.axis_font_size_entry)

        self.tick_mark_size_label = QLabel("tick marks:")
        text_override_layout.addWidget(self.tick_mark_size_label)

        self.tick_mark_size_entry = QLineEdit()
        self.tick_mark_size_entry.setText(str(self.tick_mark_size))
        text_override_layout.addWidget(self.tick_mark_size_entry)

        layout.addWidget(text_override_group)

        self.fig_btn = QPushButton("Generate Figure")
        self.fig_btn.clicked.connect(self.generate_figure)
        layout.addWidget(self.fig_btn)

    @Slot(list)
    def search_datasets(self,query_items:list):
        self.dataset_select.clear()
        self.dataset_select.addItems(query_items)

    def refresh_datasets(self):
        self.dataset_select.clear()
        self.dataset_search.clear()
        self.dataset_names = []
        for p in self.ulg.data_list:
            self.dataset_names.append(p.name)
        self.dataset_select.addItems(self.dataset_names)
        self.dataset_search.complete_list = self.dataset_names
        self.dataset_search.query_list = self.dataset_names

    def refresh_data_keys(self):
        self.data_key_select.clear()

    def select_dataset(self):
        dataset_name = self.dataset_select.currentItem().text()
        self.dataset = self.ulg.get_dataset(dataset_name)
        self.dataset_keys = self.dataset.data.keys()
        self.fig_title = title_formatter(dataset_name)
        data_keys = []
        for d in self.dataset_keys:
            data_keys.append(d)
        self.data_key_select.clear()
        self.data_key_select.addItems(data_keys)

    def select_data_key(self):
        self.data_key = self.data_key_select.currentItem().text()
        self.y_label = title_formatter(self.data_key)

    def select_log_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Thrust Curve Filepath","","Pixhawk Log Files (*.ulg)")
        self.file_path_lbl.setText("Log File: " + file_path)
        self.ulg = ULog(file_path)
        self.refresh_datasets()
        self.refresh_data_keys()
        self.data_key = None

        status_dataset = self.ulg.get_dataset('vehicle_status')
        time_ary = status_dataset.data['timestamp']
        self.time_armed = (time_ary[-1] - time_ary[0])/1e6

        takeoff_state = status_dataset.data['takeoff_time']
        for t in takeoff_state:
            if t != 0:
                takeoff_time = t 
                break
        for i in range(len(time_ary)-1,0,-1):
            if time_ary[i] != 0:
                landing_time = time_ary[i] 
                break
        self.ToF = (landing_time - takeoff_time)/1e6


    def generate_figure(self):
        try:
            data = self.dataset.data[self.data_key]
        except (KeyError,AttributeError):
            return

        if self.num_samples_btn.isChecked():
            self.x_label = "Samples"
            x = range(len(data))
        elif self.armed_time_btn.isChecked():
            self.x_label = "Time Armed (s)"
            x = np.linspace(0,self.time_armed,len(data))
        else:
            self.x_label = "Time in Flight (s)"
            x = np.linspace(0,self.ToF,len(data))


        self.title_font_size = float(self.title_font_size_entry.text())
        self.axis_font_size = float(self.axis_font_size_entry.text())
        self.tick_mark_size = float(self.tick_mark_size_entry.text())

        plt.figure()
        plt.plot(x, data)
        plt.tick_params(axis='both', labelsize=self.tick_mark_size)
        plt.xlabel(self.x_label, fontsize=self.axis_font_size)
        plt.ylabel(self.y_label, fontsize=self.axis_font_size)
        plt.title(self.fig_title, fontsize=self.title_font_size)
        plt.grid(True)
        plt.show()

app = QApplication()
window = Main()
window.show()
app.exec()