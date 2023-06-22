import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import shutil
from contextlib import suppress
import requests
from PIL import Image


# file imports
import beaglebone_commands
from datetime import datetime

class Database:
    def __init__(self):
        self.dictionary = defaultdict(Bird)

    def __str__(self):
        return str(self.dictionary)

    def add(self, species, timestamp, confidence):
        self.dictionary[species].timestamps.append(timestamp)
        self.dictionary[species].confidences.append(confidence)
        self.dictionary[species].occurrences += 1


class Bird:
    def __init__(self):
        self.occurrences = 0
        self.timestamps = []  # list of tuples with month, day, hour, minute
        self.confidences = []

    def average_confidence(self):
        return sum(self.confidences) / self.occurrences


#  function to analyze all files in the input folder
def analyzeFiles():
    inputFolder = "--i /Users/orionmclain/BirdNET-Analyzer/Audio_Inputs "
    outputFolder = "--o /Users/orionmclain/BirdNET-Analyzer/Audio_Outputs "
    minConfidence = " --min_conf 0.70"
    coordinates = "--lat 42.375801 --lon -72.519867 "
    curWeek = "--week " + str((datetime.now()-datetime(2023, 1, 1)).days//7)
    # run all files
    os.system("python3 analyze.py "+ inputFolder + outputFolder + minConfidence + " --rtype csv " + coordinates + curWeek)

    
    

def analyzeTestFiles():
    inputFolderSingles = "--i /Users/orionmclain/BirdNET-Analyzer/Audio_Inputs_Singles "
    outputFolderSingles = "--o /Users/orionmclain/BirdNET-Analyzer/Audio_Outputs_Singles "
    minConfidence = " --min_conf 0.40"
    coordinates = "--lat 42.375801 --lon -72.519867 "
    curWeek = "--week " + str((datetime.now()-datetime(2023, 1, 1)).days//7)
    
    # run on specific files
    os.system("python3 analyze.py "+ inputFolderSingles + outputFolderSingles + minConfidence + " --rtype csv " + coordinates + curWeek)
    
    #run filtered audio
    #os.system("python3 analyze.py --i /Users/orionmclain/BirdNET-Analyzer/Filtered_Audio --o /Users/orionmclain/BirdNET-Analyzer/Filtered_Outputs  --min_conf 0.20 --rtype csv --lat 42.375801 --lon -72.519867")



############# Database and Reporting

def createDatabase():
    folder_path = '/Users/orionmclain/BirdNET-Analyzer/Audio_Outputs'
    birdnet_path = '/Users/orionmclain/BirdNET-Analyzer'
    database = Database()
    os.chdir(folder_path)
    
    count = 0
    for filename in os.listdir(folder_path):
        if count == 0: 
            date = (os.path.splitext(filename)[0]).split('_')
            dateToday = date[0] + "-" + date[1]
            try:
                with open(filename, 'r') as file:
                        if os.stat(filename).st_size == 57:
                            os.remove(filename)
                            continue
                        dateList = (os.path.splitext(filename)[0]).split('_')
                        #print(os.path.splitext(filename)[0])
                        #print(file)
                        reader = csv.reader(file)
                        #print(reader)
                        next(reader)
                        #print(reader)
                        for row in reader:
                            #print(row)
                            database.add(
                                row[3], (int(dateList[0]), int(dateList[1]), int(dateList[2]), int(dateList[3])), float(row[4]),
                            )
            except UnicodeDecodeError:
                continue
            count += 1

        else:
            #date = os.path.getmtime(filename)
            try:
                with open(filename, 'r') as file:
                    if os.stat(filename).st_size == 57:
                        os.remove(filename)
                        continue
                    dateList = (os.path.splitext(filename)[0]).split('_')
                    #print(os.path.splitext(filename)[0])
                    #print(file)
                    reader = csv.reader(file)
                    #print(reader)
                    next(reader)
                    #print(reader)
                    for row in reader:
                        #print(row)
                        database.add(
                            row[3], (int(dateList[0]), int(dateList[1]), int(dateList[2]), int(dateList[3])), float(row[4]),
                        )
                            
                            
            except UnicodeDecodeError:
                continue
    os.chdir(birdnet_path) 
    #for species, bird in database.dictionary.items():
        #print(species, bird.average_confidence(), bird.timestamps)
        #print(max(bird.confidences))
    makeDailyCSV(database, dateToday)
    plot_occurrences(database, dateToday)
    plot_average_confidences(database, dateToday)
    plot_highest_confidences(database, dateToday)
    identifyTop5Birds()




def makeDailyCSV(database, dateToday):
    dailyCSV = "/Users/orionmclain/BirdNET-Analyzer/MasterCSVs/" + dateToday + "_master.csv"
    #print(dailyCSV)
    if os.path.exists(dailyCSV):
        os.remove(dailyCSV)
    sorted_birds = sorted(database.dictionary.items(), key=lambda x: x[1].occurrences, reverse=True)
    with open(dailyCSV, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(["Species Name", "Highest Confidence", "Time of Highest Confidence", "Average Confidence", "Occurrences"])
        for species, bird in sorted_birds:
            maxConf = max(bird.confidences)
            maxConfPct = str(round(100*max(bird.confidences), 2)) + "%"
            maxConfIndex = bird.confidences.index(maxConf)
            if bird.timestamps[maxConfIndex][2] < 12:
                AMPM = " AM"
            else:
                AMPM = " PM"
            if (bird.timestamps[maxConfIndex][2])%12 == 0:
                time = 12
            else:
                time = (bird.timestamps[maxConfIndex][2])%12
            highConfTime = str(time) + ":" + f'{bird.timestamps[maxConfIndex][3]:02d}' + AMPM
            avgConfPct = str(round(100*bird.average_confidence(), 2)) + "%"
            writer.writerow([species, maxConfPct , highConfTime, avgConfPct, bird.occurrences])

    #with suppress(shutil.Error):
       # shutil.move(dailyCSV, "/Users/orionmclain/BirdNET-Analyzer/MasterCSVs")
            

def get_bird_image(bird_name):
    if not os.path.exists(os.path.join('C:', os.sep, 'Users', 'orionmclain', 'BirdNET-Analyzer', 'Google_Images', f'{bird_name}.jpg')):
        # Set up Unsplash API credentials and endpoint
        access_key = 'S9wwjFLz58B7Wsp9hq7XGhk2BeMyDeXEDlUxuYv6nK4'
        url = 'https://api.unsplash.com/search/photos'

        # Set up search parameters
        params = {
            'query': bird_name + ' close up',
            'per_page': '1'  # number of results to return
        }

        # Send GET request to Unsplash API and extract image URL from response
        response = requests.get(url, params=params, headers={'Authorization': f'Client-ID {access_key}'})

        if response.status_code == 200:
            results = response.json()['results']
            if results:
                image_url = results[0]['urls']['regular']
                image_data = requests.get(image_url).content
                save_path = os.path.join('C:', os.sep, 'Users', 'orionmclain', 'BirdNET-Analyzer', 'Google_Images', f'{bird_name}.jpeg')
                with open(save_path, 'wb') as f:
                    f.write(image_data)
            else:
                print('No results found for search query')
        else:
            print('Error occurred while querying Unsplash API') 


def identifyTop5Birds():   # returns [bird1, bird2, bird3, bird4, bird5] | birdX = (bird, high confidence, # occurrences)
    folder_path = "/Users/orionmclain/BirdNET-Analyzer/MasterCSVs"
    birdnet_path = '/Users/orionmclain/BirdNET-Analyzer'

    os.chdir(folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            if filename != '.DS-Store_master.csv':
                try:
                    with open(filename, 'r') as file:
                            #print(filename)
                            fileDate = filename.split('_')[0]
                            topOccurrences = []
                            #print(fileDate)
                            #print(os.path.splitext(filename)[0])
                            #print(file)
                            reader = csv.reader(file)
                            next(reader)
                            #print(reader)
                            # Sort the remaining rows by the  column
                            sorted_rows = sorted(reader, key=lambda row: float(row[1].replace('%', '')), reverse = True)   # sort rows according to highest confidence
                            #print("sorted_rows: ")
                            #print(sorted_rows)
                            if len(sorted_rows) < 5:
                                for i in range(len(sorted_rows)):

                                    #print(sorted_rows[i])
                                    birdName = sorted_rows[i][0]
                                    occurrences = sorted_rows[i][4]
                                    highConf = sorted_rows[i][1]
                                    highConfTime = sorted_rows[i][2]
                                    bird = [birdName, occurrences, highConf, highConfTime]
                                    #bird = [birdName, highConf]
                                    topOccurrences.append(bird)
                            else: 
                                for i in range(5):

                                    #print(sorted_rows[i])
                                    birdName = sorted_rows[i][0]
                                    occurrences = sorted_rows[i][4]
                                    highConf = sorted_rows[i][1]
                                    highConfTime = sorted_rows[i][2]
                                    bird = [birdName, occurrences, highConf, highConfTime]
                                    #bird = [birdName, highConf]
                                    topOccurrences.append(bird)
                            #print("top occurrences: ")
                    #print(topOccurrences)
                    generate_visual_aid(topOccurrences, fileDate)
                except UnicodeDecodeError:
                    continue
        
    os.chdir(birdnet_path) 
    

def generate_visual_aid(occurrences, fileDate):   # occurences = [(bird, number of occurrences, highest confidence, time of high conf)] for each 5 birds
    # Create a list of the five bird tuples and sort by confidence
    #occurrences = [occurrence1, occurrence2, occurrence3, occurrence4, occurrence5]
    # occurrences.sort(key=lambda x: x[1], reverse=True)

    # Search the image directory for each bird and add it to a list
    images = []
    for occurrence in occurrences:
        bird_path = os.path.join("/Users/orionmclain/BirdNET-Analyzer/Google_Images", f"{occurrence[0]}.jpeg")
        if os.path.exists(bird_path):
            #images.append((occurrence[0], occurrence[1], Image.open(bird_path)))
            images.append((occurrence[0], occurrence[1], occurrence[2], occurrence[3], Image.open(bird_path)))
        else:
            get_bird_image(occurrence[0])
            #images.append((occurrence[0], occurrence[1], Image.open(bird_path)))
            images.append((occurrence[0], occurrence[1], occurrence[2], occurrence[3], Image.open(bird_path)))

    # Create a figure with five subplots
    #plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 17))
    fig.patch.set_facecolor('#152238')
    gs = GridSpec(5, 1, figure=fig, hspace=0)

    for i, (bird, birdOccurrences, confidence, time, image) in enumerate(images):
        gs_bird = gs[i].subgridspec(2, 1, height_ratios=[7, 1], hspace=0.5)

        # Add the image to the upper subplot
        axs_image = fig.add_subplot(gs_bird[0])
        axs_image.imshow(image)
        axs_image.axis("off")

        # Add the title to the lower subplot
        axs_title = fig.add_subplot(gs_bird[1])
        axs_title.set_title(f"{i+1}. {bird}\n Max Confidence of {confidence} at {time}, {birdOccurrences} Total Identifications", fontsize=16, fontweight="bold", color='white')
        axs_title.axis("off")
    
    # Add a title to the figure
    fig.suptitle("Top 5 Birds Identified: " + fileDate + "-2023", fontsize=20, fontweight="bold", color='white')

    # Adjust the spacing and size of the subplots
    plt.subplots_adjust(top=0.95, bottom=0.02, hspace=0.2)

    plt.savefig("/Users/orionmclain/BirdNET-Analyzer/Top_5_Charts/" + fileDate + "_Top5.png")




def plot_occurrences(database, dateToday):
    figure = plt.figure(figsize=(14, 7))
    species = list(database.dictionary.keys())
    plt.rcParams.update({'font.size': 12})
    #print(species)
    confidences = [bird.occurrences for bird in database.dictionary.values()]
    plt.barh(species, confidences)
    plt.xlabel("Occurrences")
    plt.ylabel("Species")
    plt.title("Occurrences of Each Species " + dateToday)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    #plt.locator_params(axis="y", nbins=4)
    plt.show()
    figName = dateToday + '_occurrencesPlot.png'
    #figName = 'occurrencesPlot.png'
    figure.savefig("/Users/orionmclain/BirdNET-Analyzer/occurrencesPlots/" + figName)
    plt.close(figure)
    
def plot_average_confidences(database, dateToday):
    figure = plt.figure(figsize=(14, 7))
    species = list(database.dictionary.keys())
    plt.rcParams.update({'font.size': 12})
    #print(species)
    confidences = [bird.average_confidence() for bird in database.dictionary.values()]
    plt.barh(species, confidences)
    plt.xlabel("Average Confidence")
    plt.ylabel("Species")
    plt.title("Average Confidence of Each Species " + dateToday)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.show()
    figName = dateToday + '_averageConfidencesPlot.png'
    #figName = 'averageConfidencesPlot.png'
    figure.savefig("/Users/orionmclain/BirdNET-Analyzer/avgConfPlots/" + figName)
    plt.close(figure)
    #with suppress(shutil.Error):    
        #shutil.move("/Users/orionmclain/BirdNET-Analyzer/" + figName, "/Users/orionmclain/BirdNET-Analyzer/avgConfPlots")

def plot_highest_confidences(database, dateToday):
    figure = plt.figure(figsize=(14, 7))
    species = list(database.dictionary.keys())
    highConf = [max(bird.confidences) for bird in database.dictionary.values()]
    plt.rcParams.update({'font.size': 12})
    plt.barh(species, highConf)
    plt.xlabel("Highest Confidence")
    plt.ylabel("Species")
    plt.title("Highest Confidence of Each Species " + dateToday)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.show()
    figName = dateToday + '_highestConfidencesPlot.png'
    figure.savefig("/Users/orionmclain/BirdNET-Analyzer/highConfPlots/" + figName)
    plt.close(figure)
    
    



    #def move_old_data():
        #os.mkdir("/Users/orionmclain/BirdNET-Analyzer/Audio_Inputs")

if __name__ == "__main__":
    #beaglebone_commands.download_data()   # 
    
    #audio_filtering.bandpassFilter()   # run audio filter on data
    
    #audio_filtering.moveFilteredAudio() 
    
    #analyzeFiles()                  # run analysis of input audio, results stored in Audio_Outputs folder
    
    createDatabase()                # create database and reports

    #get_bird_image('Northern Cardinal')

    #identifyTop5Birds() 

    #feeder_gui.gui()                # gui for program 
