import pandas as pd
import numpy as np

class TopicContent:

    def __init__(self, path):

        if type(path) == pd.core.frame.DataFrame:
            self.df = path

        elif path[-3:] == "csv":
            self.df = pd.read_csv(path)

        elif path[-4:] == "xlsx":
            self.df = pd.read_excel(path)

        self.title_content = dict([])

        if (self.df.get("Title").iloc[0] == 0):
            self.title_content["Unnamed"] = []

        topics = self.get_topics()

        self.title_info = []

        for topic in topics:
            corresponding_font_size = round(np.max(self.df[self.df.get(
                "text")==topic].get("font_sizes")))
            self.title_info.append((topic,corresponding_font_size))
            self.title_content[topic] = []

        rows = self.df.shape[0]

        latest_topic = "Unnamed"
        for i in range(rows):
            text = self.df.get("text").iloc[i]
            is_topic = self.df.get("Title").iloc[i]
            font_size = self.df.get("font_sizes").iloc[i]

            if is_topic:
                latest_topic = text

            else:
                self.title_content[latest_topic].append(text)




    def get_topics(self):
        all_topics = list(self.df[self.df.get("Title") == 1].get("text"))
        indexes = np.unique(all_topics, return_index=True)[1]
        topics = [all_topics[index] for index in sorted(indexes)]
        return topics



    def get_dict(self):
        return self.title_content

    def get_index(self):
        unique_fonts = np.unique([grouped[1] for grouped in self.title_info])
        unique_fonts = list(unique_fonts)[::-1]

        index_str = ""

        for group in self.title_info:
            index_str += "\n"
            index_str += "#"*unique_fonts.index(group[1]) + " " + group[0]

        return index_str


#obj = TopicContent("/Users/rohanraval/Desktop/PlayingAround/TrainData"
 #                  "/javanotesUSE.xlsx")
#print(obj.print_dict())
#obj.get_topic_dataframe()
#print(list(topic_df["font_sizes"]))
#print(obj.get_topics())
#print(obj.get_index())



