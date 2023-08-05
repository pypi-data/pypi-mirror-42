from pyspark.sql import Row
from ElasticSearchSparkLoader import load_elasticsearch

# Generate RDD
example_dataset = sc.parallelize([ \
    Row(id=1, name='Foo'),
    Row(id=2, name='Bar'),
])

# Also works on DataFrames
# example_dataset = example_dataset.toDF()

# Perform ElasticSearch Load
load_elasticsearch(
    example_dataset,
    # ElasticSearch Master Host
    '35.193.123.45',
    # ElasticSearch Port
    '9200',
    # Index Name
    'examples',
    # Document Type
    'example',
    # Name of ID field in Dataset
    'id'
)

