# -*- coding: utf-8 -*-
"""MovieAnalyticsTool.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YfgIAnR3-qqtiQ63hPsmso5tF7JSlvNC
"""

'''Kayla Danao - Movie Analytics Tool
This program allows a user to pick a movie and choose between 5 analytic options:
Background, Reception, Poster, Wordcloud, and Sentiment. This program utilizes 
the OMDb API and the MIS 515 API for IMDb movie reviews. The user can run the
program as many times as desired'''

!pip install xmltodict
import requests, wordcloud, xmltodict, matplotlib.pyplot as plt, skimage.io, json, textblob

run = "yes"

print("Welcome to the movie analytics tool!\n")

while run == "yes":
    movie = input("What movie would you like to analyze? ")

    base_url = "https://www.omdbapi.com/?r=xml&apikey=809348ae&t="
    full_url = base_url + movie

    response = requests.get(full_url)

    if response:
        analysis = input("What would you like to see (background/reception/poster/wordcloud/sentiment)? ")
        analysisBlob = textblob.TextBlob(analysis) 
        analysis = analysisBlob.lower().correct() #lower case and correct input

        data = xmltodict.parse(response.text)
        
        if analysis == "background": #gets background information of input movie from API
            year = data["root"]["movie"]["@year"]
            rating = data["root"]["movie"]["@rated"]
            runtime = data["root"]["movie"]["@runtime"]
            genre = data["root"]["movie"]["@genre"]
            actors = data["root"]["movie"]["@actors"]
            plot = data["root"]["movie"]["@plot"]
            print("\nYear:", year, "\nRating:", rating, "\nRuntime:", runtime, 
                  "\nGenre:", genre, "\nActors:", actors, "\nPlot:", plot)
            
            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct() 
        
        elif analysis == "reception": #gets reception from API 
            awards = data["root"]["movie"]["@awards"]
            metascore = data["root"]["movie"]["@metascore"]
            imdb = data["root"]["movie"]["@imdbRating"]
            print("\nAwards:", awards, "\nMetascore:", metascore, "\nIMDb rating:", imdb)

            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct()
        
        elif analysis == "poster": #gets poster image url from API and shows to screen
            poster_url = data["root"]["movie"]["@poster"]
            image = skimage.io.imread(poster_url)
            plt.imshow(image, interpolation = "bilinear")
            plt.axis("off")
            plt.show(block = False)
            plt.pause(0.1)
            plt.close()

            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct()

        elif analysis == "wordcloud": #produces wordcloud based on reviews of the movie
            reviews_url = "https://dgoldberg.sdsu.edu/515/imdb/"+movie.lower()+".json"
            # print(reviews_url)
            response2 = requests.get(reviews_url)
            if response2:
                imdbData = json.loads(response2.text)
                #print(json.dumps(imdbData, indent = 4))

                text = ""
                for line in imdbData:
                    review = line["Review text"]
                    text = text + review + " "
                    # print(text)

                cloud = wordcloud.WordCloud(width = 2000, height = 2000, colormap = "inferno")
                cloud.generate(text)

                plt.imshow(cloud, interpolation = "bilinear")
                plt.axis("off")
                plt.show(block = False)
                plt.pause(0.1)
                plt.close()
            else:
                print("Sorry, connection error.")

            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct()
        
        elif analysis == "sentiment": #sentiment analysis of movie based on reviews
            reviews_url = "https://dgoldberg.sdsu.edu/515/imdb/"+movie.lower()+".json"
            # print(reviews_url)
            response2 = requests.get(reviews_url)
            if response2:
                imdbData = json.loads(response2.text)
                #print(json.dumps(imdbData, indent = 4))

                text = ""
                for line in imdbData:
                    review = line["Review text"]
                    text = text + review + " "
                    # print(text)
                
                blob = textblob.TextBlob(text)
                print("\nAverage IMDb review polarity:", blob.polarity)
                print("Average IMDb review subjectivity:", blob.subjectivity)
            else:
                print("Sorry, the tool could not successfully load any IMDb reviews for this movie. Please try another analysis or movie.")

            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct()

        else: #error output
            print("\nSorry, that analysis is not supported. Please try again.")
            run_fix = input("\nWould you like to run another analysis (yes/no)? ")
            run_fix = textblob.TextBlob(run_fix)
            run = run_fix.lower().correct()

    else:
        ("Sorry, connection error.")