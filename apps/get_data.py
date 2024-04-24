import sqlite3
import os
import pandas as pd
import nltk
from wordcloud import WordCloud, STOPWORDS
import re
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class sqlHelper(object):
  def __init__(self):
      basedir = os.path.abspath(os.path.dirname(__file__))
      db_file = os.path.join(basedir, 'datascalp')
      self.conn = sqlite3.connect(db_file)
      def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
      self.conn.row_factory = dict_factory
      self.cursor = self.conn.cursor()
  
  def close(self):
    self.cursor.close()
    self.conn.close()

  def get_stock_list(self):
      sql = "SELECT * FROM stock_list;"
      self.cursor.execute(sql)
      stock_list = self.cursor.fetchall()
      return stock_list

  def get_heat_map_data(self):
      startDate = "2021-09-24"
      endDate = "2021-10-01"
      sql = '''
            SELECT date(tr.date) AS x, ts.stock_id AS stockId, sl.Name AS y,
            CASE 
                WHEN ROUND(avg(flair_score), 2) BETWEEN -1.0 AND -0.35 THEN 'NEGATIVE'
                WHEN ROUND(avg(flair_score), 2) BETWEEN -0.35 AND 0.35 THEN 'NEUTRAL'
                ELSE 'POSITIVE'
            END AS sentiment,
            ROUND(avg(flair_score), 2) AS flair
            FROM twitter_score ts JOIN twitter_raw tr ON ts.message_id = tr.id
            JOIN stock_list sl ON sl.stockID = ts.stock_id
            WHERE tr.date between '{startDate}' and '{endDate}'
            GROUP BY date(date), ts.stock_id;'''.format(startDate=startDate, endDate=endDate)

      self.cursor.execute(sql)
      heat_map_data = self.cursor.fetchall()
      return heat_map_data

  def get_bar_chart_data(self, stock_id):
      sql1 = """
      select count(merge.new_score) positive from 
      (select strftime('%m/%d/%Y',raw.date)  as new_date, (score.nltk_score+score.textblob_score+score.flair_score+score.bert_score) new_score
      from twitter_raw raw, twitter_score score
      where raw.id = score.message_id and score.stock_id = {} and new_date BETWEEN '09/24/2020' and '09/30/2021' and new_score>0) merge
      group by new_date
      """.format(stock_id)
      self.cursor.execute(sql1)
      df_positive = pd.DataFrame(self.cursor.fetchall())
      df_positive.columns = ['positive']
      positive_list = df_positive['positive'].to_list()
      sql2 = """
            select count(merge.new_score) positive from 
      (select strftime('%m/%d/%Y',raw.date)  as new_date, (score.nltk_score+score.textblob_score+score.flair_score+score.bert_score) new_score
      from twitter_raw raw, twitter_score score
      where raw.id = score.message_id and score.stock_id = {} and new_date BETWEEN '09/24/2020' and '09/30/2021' and new_score<0) merge
      group by new_date
            """.format(stock_id)
      self.cursor.execute(sql2)
      df_negative = pd.DataFrame(self.cursor.fetchall())
      df_negative.columns = ['negative']
      negative_list = df_negative['negative'].to_list()
      return positive_list, negative_list

  def get_word_cloud_data(self, stock_id):
      nltk.download('stopwords')
      startDate = "2021-09-24"
      endDate = "2021-09-30"
      getMessage = '''SELECT substr(date, 1, 10) as create_date, tweet FROM twitter_raw 
                         WHERE create_date between '{startDate}' and '{endDate}'
                         AND stockID = {stockID};'''.format(startDate=startDate, endDate=endDate, stockID=stock_id)
      self.cursor.execute(getMessage)
      df = pd.DataFrame(self.cursor.fetchall())
      tweet = []

      def clean_tweet(tweet):
          if type(tweet) == np.float64:
              return ""
          stopwords = nltk.corpus.stopwords.words('english')
          temp = tweet.lower()
          temp = re.sub("'", "", temp)  # to avoid removing contractions in english
          temp = re.sub("@[A-Za-z0-9_]+", "", temp)
          temp = re.sub("#[A-Za-z0-9_]+", "", temp)
          temp = re.sub(r'http\S+', '', temp)
          temp = re.sub('[()!?]', ' ', temp)
          temp = re.sub('\[.*?\]', ' ', temp)
          temp = re.sub("[^a-z0-9]", " ", temp)
          temp = temp.split()
          temp = [w for w in temp if not w in stopwords]
          temp = " ".join(word for word in temp)
          return temp

      for x in range(len(df)):
          temp = clean_tweet(df['tweet'][x])
          temp = temp.split(" ")
          for word in temp:
              tweet.append(word)

      tweet = " ".join(word for word in tweet)
      plt.subplots(1, 1, figsize=(6, 6))
      wc_b = WordCloud(stopwords=STOPWORDS,
                       background_color="white", max_words=50,
                       max_font_size=256, random_state=42,
                       width=600, height=600)
      wc_b.generate(tweet)
      s = io.BytesIO()

      plt.imshow(wc_b, interpolation="bilinear")
      plt.axis('off')
      plt.savefig(s, format='png')
      s.seek(0)

      s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
      return s
  
  def get_time_line_data_trend(self, stock_id):

      getMessage = '''select avg(ts.flair_score) as avg_score,  case WHEN Next_day_Trend='Increase' THEN 1 else -1 END as TREND
      from  yahoo_finance_with_trend yf 
      join twitter_raw tr on yf.stock_id=tr.stockID and yf.CLOSING_DATE=strftime('%m/%d/%Y',tr.date) 
      join twitter_score ts on tr.id=ts.message_id and tr.stockID=ts.stock_id
      where tr.stockID={stockID} and yf.CLOSING_DATE between '09/22/2020' and '09/30/2021'
      group by tr.stockID,yf.CLOSING_DATE,yf.Next_day_Trend 
      order by yf.CLOSING_DATE
      ;'''. format(stockID=stock_id)
      self.cursor.execute(getMessage)
      timeline_df = pd.DataFrame(self.cursor.fetchall())
      print(timeline_df)
      return timeline_df['TREND'].to_list()

  def get_time_line_data_avg_score(self, stock_id):

      getMessage = '''select avg(ts.flair_score) as avg_score,  case WHEN Next_day_Trend='Increase' THEN 1 else -1 END as TREND
       from  yahoo_finance_with_trend yf 
       join twitter_raw tr on yf.stock_id=tr.stockID and yf.CLOSING_DATE=strftime('%m/%d/%Y',tr.date) 
       join twitter_score ts on tr.id=ts.message_id and tr.stockID=ts.stock_id
       where tr.stockID={stockID} and yf.CLOSING_DATE between '09/22/2020' and '09/30/2021'
       group by tr.stockID,yf.CLOSING_DATE,yf.Next_day_Trend 
       order by yf.CLOSING_DATE
       ;'''.format(stockID=stock_id)
      self.cursor.execute(getMessage)
      timeline_df = pd.DataFrame(self.cursor.fetchall())
      return timeline_df['avg_score'].to_list()

  def get_tweet_display_data(self, stock_id):
      startDate = "2021-09-30"
      endDate = "2021-09-30"
      getMessage = '''SELECT substr(date, 1, 10) as create_date, tweet FROM twitter_raw 
                               WHERE create_date between '{startDate}' and '{endDate}'
                               AND stockID = {stockID} LIMIT 20;'''.format(startDate=startDate, endDate=endDate,
                                                                  stockID=stock_id)
      self.cursor.execute(getMessage)
      df = pd.DataFrame(self.cursor.fetchall())
      result = []
      result.append(df['create_date'].to_list())
      result.append(df['tweet'].to_list())
      return result

  def get_emotion_graph_data(self, stock_id):
      getMessage = '''SELECT flair_score, arouse_score FROM twitter_score AS ts JOIN twitter_raw AS tr 
      WHERE ts.message_id = tr.id AND ts.stock_id ={stockID} and strftime('%m/%d/%Y',tr.date) = '09/30/2021'
      ;'''.format(stockID=stock_id)
      self.cursor.execute(getMessage)
      stock_list = pd.DataFrame(self.cursor.fetchall())
      pairs = list(zip(stock_list['flair_score'], stock_list['arouse_score']))
      outputDict = []
      for pair in pairs:
          curCordinate = {'x' : round(pair[0],2), 'y': round(pair[1],2)}
          outputDict.append(curCordinate)
      # print(outputDict)
      return outputDict

  def get_stock_table_data(self, stock_id):
      pass


#   def get_twitter_score(self, stock_id):
#       self.cursor.execute("SELECT * FROM twitter_score WHERE stock_id=? LIMIT 1000", [stock_id])
#       top_1000_twitter_score = self.cursor.fetchall()
#       return top_1000_twitter_score
  
#   def get_twitter_raw(self, stock_id):
#       self.cursor.execute("SELECT * FROM twitter_raw WHERE stockID=? LIMIT 1000", [stock_id])
#       top_1000_twitter_raw = self.cursor.fetchall()
#       return top_1000_twitter_raw
  
#   def get_yahoo_finance_with_trend(self, stock_id):
#       self.cursor.execute("SELECT * FROM yahoo_finance_with_trend WHERE STOCK_ID=? LIMIT 100", [stock_id])
#       top_100_yahoo_finance_trend = self.cursor.fetchall()
#       return top_100_yahoo_finance_trend
