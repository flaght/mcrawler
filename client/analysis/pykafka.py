from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer1 = KafkaConsumer('newsparser_task_algo',
                         group_id='my-group',
                         bootstrap_servers=['192.168.1.85:9091'])
consumer2 = KafkaConsumer('newsparser_task_algo',
                         group_id='my-group',
                         bootstrap_servers=['192.168.1.80:9091'])
consumer3 = KafkaConsumer('newsparser_task_algo',
                         group_id='my-group',
                         bootstrap_servers=['192.168.1.81:9091'])

for message in consumer1:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
for message in consumer2:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

for message in consumer3:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))