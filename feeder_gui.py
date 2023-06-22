import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMessageBox

from beaglebone_commands import download_data, removeFiles
from main import analyzeFiles, createDatabase, get_bird_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Who's Hoo")

        # Set the window state to maximized
        self.setWindowState(Qt.WindowMaximized)

        # Create a tab widget
        self.tab_widget = QTabWidget()
        #self.tab_widget.setFont(QFont('Times', 16))
        self.setCentralWidget(self.tab_widget)


        # Create the Home tab
        self.home_tab = QWidget()
        self.home_label = QLabel()
        pixmap = QPixmap("/Users/orionmclain/BirdNET-Analyzer/logo.png")
        self.home_label.setPixmap(pixmap)
        self.home_tab.layout = QVBoxLayout()
        self.home_tab.layout.addWidget(self.home_label)
        self.home_tab.layout.setAlignment(Qt.AlignCenter) # Center the label widget
        self.home_tab.setLayout(self.home_tab.layout)
        
        self.tab_widget.addTab(self.home_tab, "Home")

    
        # ----- Create the top 5 birds report tab ------ 

        self.top5_tab = QWidget()
        self.top5_label = QLabel()
        self.top5_label.setObjectName("top5_label") # add a unique name to the label
        
        # Create a scroll area widget to contain the plots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)
        self.top5_tab.layout = QVBoxLayout()

        # Iterate through the plots in the directory and add them to the scroll area layout
        top5_dir = "/Users/orionmclain/BirdNET-Analyzer/Top_5_Charts"
        top5List = os.listdir(top5_dir)
        top5List.sort(reverse = True)
        for file_name in top5List:
            if file_name.endswith(".png"):
                top5_path = os.path.join(top5_dir, file_name)
                top5_label = QLabel()
                pixmap = QPixmap(top5_path)
                pixmap_scaled = pixmap.scaledToWidth(1000, Qt.SmoothTransformation)
                top5_label.setPixmap(pixmap_scaled)
                top5_label.setAlignment(Qt.AlignCenter)
                scroll_area_layout.addWidget(top5_label)

        # Add the scroll area to the top 5 birds tab layout
        self.top5_tab.layout.addWidget(scroll_area)

        self.top5_tab.layout.addWidget(self.top5_label)
        self.top5_tab.layout.setAlignment(Qt.AlignCenter) # Center the label widget
        self.top5_tab.setLayout(self.top5_tab.layout)
        self.tab_widget.addTab(self.top5_tab, "Top 5 Birds Reports")



        # ----- Create the Occurrences Report tab -----

        self.occurrences_tab = QWidget()
        self.occurrences_label = QLabel()
        self.occurrences_label.setObjectName("occurrences_label") # add a unique name to the label
        
        # Create a scroll area widget to contain the plots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)
        self.occurrences_tab.layout = QVBoxLayout()

        # Iterate through the plots in the directory and add them to the scroll area layout
        occurrences_dir = "/Users/orionmclain/BirdNET-Analyzer/occurrencesPlots"
        occurrencesList = os.listdir(occurrences_dir)
        occurrencesList.sort(reverse = True)
        for file_name in occurrencesList:
            if file_name.endswith(".png"):
                occurrences_path = os.path.join(occurrences_dir, file_name)
                occurrences_label = QLabel()
                pixmap = QPixmap(occurrences_path)
                pixmap_scaled = pixmap.scaledToWidth(1000, Qt.SmoothTransformation)
                occurrences_label.setPixmap(pixmap_scaled)
                occurrences_label.setAlignment(Qt.AlignCenter)
                scroll_area_layout.addWidget(occurrences_label)

        # Add the scroll area to the occurrences tab layout
        self.occurrences_tab.layout.addWidget(scroll_area)

        self.occurrences_tab.layout.addWidget(self.occurrences_label)
        self.occurrences_tab.layout.setAlignment(Qt.AlignCenter) # Center the label widget
        self.occurrences_tab.setLayout(self.occurrences_tab.layout)
        self.tab_widget.addTab(self.occurrences_tab, "Occurrences Report")
 

        # ----- Create the Average Confidence Report tab -----

        self.averageConfidence_tab = QWidget()
        self.averageConfidence_label = QLabel()
        self.averageConfidence_label.setObjectName("averageConfidence_label") # add a unique name to the label
        
        # Create a scroll area widget to contain the plots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)
        self.averageConfidence_tab.layout = QVBoxLayout()


        # Iterate through the plots in the directory and add them to the scroll area layout
        avgConf_dir = "/Users/orionmclain/BirdNET-Analyzer/avgConfPlots"
        avgConfList = os.listdir(avgConf_dir)
        avgConfList.sort(reverse = True)
        for file_name in avgConfList:
            if file_name.endswith(".png"):
                avgConf_path = os.path.join(avgConf_dir, file_name)
                avgConf_label = QLabel()
                pixmap = QPixmap(avgConf_path)
                pixmap_scaled = pixmap.scaledToWidth(1000, Qt.SmoothTransformation)
                avgConf_label.setPixmap(pixmap_scaled)
                avgConf_label.setAlignment(Qt.AlignCenter)
                scroll_area_layout.addWidget(avgConf_label)

        # Add the scroll area to the avg conf tab layout
        self.averageConfidence_tab.layout.addWidget(scroll_area)

        self.averageConfidence_tab.layout.addWidget(self.averageConfidence_label)
        self.averageConfidence_tab.layout.setAlignment(Qt.AlignCenter) # Center the label widget
        self.averageConfidence_tab.setLayout(self.averageConfidence_tab.layout)
        self.tab_widget.addTab(self.averageConfidence_tab, "Average Confidence Report")



        # ----- Create the Highest Confidence Report tab -----

        self.highestConfidence_tab = QWidget()
        self.highestConfidence_label = QLabel()
        self.highestConfidence_label.setObjectName("highestConfidence_label") # add a unique name to the label
        
        # Create a scroll area widget to contain the plots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)
        self.highestConfidence_tab.layout = QVBoxLayout()

        # Iterate through the plots in the directory and add them to the scroll area layout
        highConf_dir = "/Users/orionmclain/BirdNET-Analyzer/highConfPlots"
        highConfList = os.listdir(highConf_dir)
        highConfList.sort(reverse = True)
        for file_name in highConfList:
            if file_name.endswith(".png"):
                highConf_path = os.path.join(highConf_dir, file_name)
                highConf_label = QLabel()
                pixmap = QPixmap(highConf_path)
                pixmap_scaled = pixmap.scaledToWidth(1000, Qt.SmoothTransformation)
                highConf_label.setPixmap(pixmap_scaled)
                highConf_label.setAlignment(Qt.AlignCenter)
                scroll_area_layout.addWidget(highConf_label)

        # Add the scroll area to the high conf tab layout
        self.highestConfidence_tab.layout.addWidget(scroll_area)

        self.highestConfidence_tab.layout.addWidget(self.highestConfidence_label)
        self.highestConfidence_tab.layout.setAlignment(Qt.AlignCenter) # Center the label widget
        self.highestConfidence_tab.setLayout(self.highestConfidence_tab.layout)
        self.tab_widget.addTab(self.highestConfidence_tab, "Highest Confidence Report")


        # -----  Create the Images tab  -----

        self.images_tab = QWidget()
        self.images_tab.layout = QVBoxLayout()

        # Create a scroll area widget to contain the images
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area.setWidget(scroll_area_widget)

        # Iterate through the images in the directory and add them to the scroll area layout
        image_dir = "/Users/orionmclain/BirdNET-Analyzer/Feeder_Images"
        for file_name in sorted(os.listdir(image_dir), reverse = True):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                image_path = os.path.join(image_dir, file_name)
                image_label = QLabel()
                pixmap = QPixmap(image_path)
                pixmap_scaled = pixmap.scaledToWidth(500, Qt.SmoothTransformation)
                image_label.setPixmap(pixmap_scaled)
                image_label.setAlignment(Qt.AlignCenter)
                scroll_area_layout.addWidget(image_label)

        # Add the scroll area to the images tab layout
        self.images_tab.layout.addWidget(scroll_area)

        self.images_tab.setLayout(self.images_tab.layout)
        self.tab_widget.addTab(self.images_tab, "Images")



        # ----- Create the Functions tab ----- 

        self.functions_tab = QWidget()
        self.functions_tab.layout = QHBoxLayout()
        self.functions_tab.setLayout(self.functions_tab.layout)
        self.tab_widget.addTab(self.functions_tab, "System Functions")

        # Add button to automate all feeder functions
        universal_button = QPushButton("Automate All Functions")
        universal_button.setFont(QFont('Times', 18))
        universal_button.setFixedSize(250, 200)
        universal_button.clicked.connect(self.universalButton)
        self.functions_tab.layout.addWidget(universal_button)

        # Add button to download data
        download_button = QPushButton("Transfer Data From Feeder")
        download_button.setFont(QFont('Times', 18))
        download_button.setFixedSize(250, 200)
        download_button.clicked.connect(self.downloadButton)
        self.functions_tab.layout.addWidget(download_button)

        # Add button to analyze files
        analyze_button = QPushButton("Analyze Audio Files")
        analyze_button.setFont(QFont('Times', 18))
        analyze_button.setFixedSize(250, 200)
        analyze_button.clicked.connect(self.analyzeFilesButton)
        self.functions_tab.layout.addWidget(analyze_button)

        # Create database button
        create_button = QPushButton("Generate Reports")
        create_button.setFont(QFont('Times', 18))
        create_button.setFixedSize(250, 200)
        create_button.clicked.connect(self.createDatabaseButton)
        self.functions_tab.layout.addWidget(create_button)

        # Create remove files button
        remove_button = QPushButton("Remove Old Feeder Files")
        remove_button.setFont(QFont('Times', 18))
        remove_button.setFixedSize(250, 200)
        remove_button.clicked.connect(removeFiles)
        self.functions_tab.layout.addWidget(remove_button)


    def universalButton(self):
        download_data()
        removeFiles()
        analyzeFiles()
        createDatabase()


        # Print message in gui that the function is completed
        msg = QMessageBox()
        msg.setWindowTitle("Function Complete")
        msg.setText("Feeder functions have finished: Data downloaded, Files analyzed, and Reports Generated")
        msg.exec_()

        # Reset the main window by closing and reopening it
        self.close()
        self.__init__()
        self.show()

    def downloadButton(self):
        download_data()
        #date_today = 
        #pixmap = QPixmap("/Users/orionmclain/BirdNET-Analyzer/Plots" +  + "_occurrencesPlot.png")
        #self.occurrences_label.setPixmap(pixmap)

         # Print message in gui that the function is completed
        msg = QMessageBox()
        msg.setWindowTitle("Function Complete")
        msg.setText("Download data function has finished.")
        msg.exec_()

        # Reset the main window by closing and reopening it
        self.close()
        self.__init__()
        self.show()


    def analyzeFilesButton(self):
        analyzeFiles()

         # Print message in gui that the function is completed
        msg = QMessageBox()
        msg.setWindowTitle("Function Complete")
        msg.setText("Analyze files function has finished.")
        msg.exec_()

    def createDatabaseButton(self):
        createDatabase() 

         # Print message in gui that the function is completed
        msg = QMessageBox()
        msg.setWindowTitle("Function Complete")
        msg.setText("Create Database function has finished.")
        msg.exec_()

        # Reset the main window by closing and reopening it
        self.close()
        self.__init__()
        self.show()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
