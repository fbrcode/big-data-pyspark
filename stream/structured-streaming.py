"""
Initiate readings from apache logs on logs directory

Every new log file will generate a new computation (status code summary)

Create the logs directory before starting spark process, if it does not exist already

Initiate the process with spark-submit structured-streaming.py

Copy provided access_log.example to logs folder, like: cp access_log.example logs/access_log.txt

Watch the summarized response status results to display on the running spark server like this... 

-------------------------------------------
Batch: 0
-------------------------------------------
+------+-----+
|status|count|
+------+-----+
|   500|10714|
|   301|  271|
|   400|    2|
|   404|   26|
|   200|64971|
|   304|   92|
|   302|    2|
|   405|    1|
+------+-----+

Sending more apache log files will increase the status log count

"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession

from pyspark.sql.functions import regexp_extract

# Create a SparkSession (the config bit is only for Windows!)
# spark = SparkSession.builder.config("spark.sql.warehouse.dir", "/tmp").appName("StructuredStreaming").getOrCreate()
spark = SparkSession.builder.appName("StructuredStreaming").getOrCreate()

# Set to warning messages only to avoid INFO messages flooding
spark.sparkContext.setLogLevel('WARN')

# Monitor the logs directory for new log data, and read in the raw lines as accessLines
accessLines = spark.readStream.text("logs")

# Parse out the common log format to a DataFrame
contentSizeExp = r'\s(\d+)$'
statusExp = r'\s(\d{3})\s'
generalExp = r'\"(\S+)\s(\S+)\s*(\S*)\"'
timeExp = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})]'
hostExp = r'(^\S+\.[\S+\.]+\S+)\s'

logsDF = accessLines.select(regexp_extract('value', hostExp, 1).alias('host'),
                         regexp_extract('value', timeExp, 1).alias('timestamp'),
                         regexp_extract('value', generalExp, 1).alias('method'),
                         regexp_extract('value', generalExp, 2).alias('endpoint'),
                         regexp_extract('value', generalExp, 3).alias('protocol'),
                         regexp_extract('value', statusExp, 1).cast('integer').alias('status'),
                         regexp_extract('value', contentSizeExp, 1).cast('integer').alias('content_size'))

# Keep a running count of every access by status code
statusCountsDF = logsDF.groupBy(logsDF.status).count()

# Kick off our streaming query, dumping results to the console
query = ( statusCountsDF.writeStream.outputMode("complete").format("console").queryName("counts").start() )

# Run forever until terminated
query.awaitTermination()

# Cleanly shut down the session
spark.stop()
