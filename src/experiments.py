import tensorflow as tf
import encoder
import model 
import sample

import os 
import json
import tweepy 
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import re

consumer_key = ''
consumer_secret = ''

access_token = ''
access_secret = ''
 

class TwittBrain( ):

	def __init__( self , encoder , model_name = "117M" , batch_size = 1 ):

		self.encoder = encoder
		self.model_name = model_name
		self.hparams =  model.default_hparams()
		with open(os.path.join('models', model_name, 'hparams.json')) as f:
			self.hparams.override_from_dict(json.load(f))
		

	def sample_sequence( self , text , length , temperature = 1.0 , top_k = 0    ):

		context_tokens = self.encoder.encode( text )


		with tf.Session( graph = tf.Graph()) as sess:
			self.X = tf.placeholder( tf.int32 , [ 1 , None ] )

			output = sample.sample_sequence(
				hparams = self.hparams , length = length , context = self.X, batch_size = 1 , temperature = temperature , top_k = top_k
			)
			saver = tf.train.Saver()
			ckpt = tf.train.latest_checkpoint(os.path.join('models', self.model_name))
			saver.restore(sess, ckpt)

			ou = sess.run( output , feed_dict = {  self.X : [context_tokens  for i in range(1)]  })

			return ou 
			#print( ou )
class Listener( StreamListener ):

	def on_data( self , data) :

		try:
			print(" Responding to twitt ")
			self.twiit( data) 
			return True 
		except BaseException as e :
			print(str(e) )

		return True

	def on_error( self , status):

		print(status)
		return True

	def getseed( self , random_state = 666 ):

		seed = "The men in black fleed throught the desert, and the gunslinger follow. "
		return seed 

	def processTweet( self , tweet , seed = "" ):

		return tweet


	def twiit( self ,data ):
		# Twiit
		#api.update_status()
		obj  = json.loads( data )

		text = obj["text"]

		if len(text) >= 140 :
			print("Extended")
			text = obj["extended_tweet"]["full_text"]


		user = obj["user"]
		sn = obj["user"]["screen_name"]
		idd = obj["id_str"]
		#tweet = "@{}  Gracias por comunicarse con AndresBot :v ".format(sn)
		#seed = self.getseed()
		#print( text )
		tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", text  ).split()) # remove mentions
		tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet , flags=re.MULTILINE) # remove urls 

		if not tweet.endswith("."):
			tweet = tweet + "."
		print("to neural network")
		print( tweet )
		tweet = tww.sample_sequence(  text , 140 )
		tweet =  enc.decode ( tweet[0] ).split(".")[1]
		
		tweet = self.processTweet( tweet  )

		api.update_status( tweet , idd  )
		print("twitt responded ")
		#print( text )
		#print( user["screen_name"] )
		return True

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
enc = encoder.get_encoder("117M")
tww = TwittBrain(  enc  )

print( "READY ")
# here goes for example the user you want to follow and respond 
track = ["@GPTResponser" ]
twiiter_stream = Stream( auth , Listener() )
twiiter_stream.filter( track = track )

