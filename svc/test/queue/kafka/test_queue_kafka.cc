//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//   Created on: 2016.12.23 Author: kerry

#include "gtest/gtest.h"
#include "logic/logic_comm.h"
#include "basic/basictypes.h"
#include "log/mig_log.h"
#include "logic/base_values.h"
#include "basic/radom_in.h"
#include <string>

class QueueKafkaTest: public testing::Test {
};

#include <ctype.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <syslog.h>
#include <sys/time.h>
#include <errno.h>
#include "rdkafka.h"

const int PRODUCER_INIT_FAILED = -1;
const int PRODUCER_INIT_SUCCESS = 0;
const int PUSH_DATA_FAILED = -1;
const int PUSH_DATA_SUCCESS = 0;


static void logger(const rd_kafka_t *rk, int level,const char *fac, const char *buf) 
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    fprintf(stderr, "%u.%03u RDKAFKA-%i-%s: %s: %s\n",
        (int)tv.tv_sec, (int)(tv.tv_usec / 1000),
        level, fac, rk ? rd_kafka_name(rk) : NULL, buf);
}


class ProducerKafka
{
public:
	ProducerKafka(){};
	~ProducerKafka(){}

	int init_kafka(int partition, char *brokers, char *topic);
	int push_data_to_kafka(const char* buf, const int buf_len);
    void destroy();

private:
	int partition_;	
	
	//rd
	rd_kafka_t* handler_;
	rd_kafka_conf_t *conf_;
	
	//topic
	rd_kafka_topic_t *topic_;
	rd_kafka_topic_conf_t *topic_conf_;
};

int ProducerKafka::init_kafka(int partition, char *brokers, char *topic)
{
	char tmp[16]={0};
	char errstr[512]={0};	

	partition_ = RD_KAFKA_PARTITION_UA;	

	/* Kafka configuration */
    conf_ = rd_kafka_conf_new();
	
	//set logger :register log function
	rd_kafka_conf_set_log_cb(conf_, logger);	
	
	/* Quick termination */
    snprintf(tmp, sizeof(tmp), "%i", SIGIO);
    rd_kafka_conf_set(conf_, "internal.termination.signal", tmp, NULL, 0);

	/*topic configuration*/
	topic_conf_ = rd_kafka_topic_conf_new();

	if (!(handler_  = rd_kafka_new(RD_KAFKA_PRODUCER, conf_, errstr, sizeof(errstr)))) 
	{
		fprintf(stderr, "*****Failed to create new producer: %s*******\n",errstr);
		return PRODUCER_INIT_FAILED;
	}

	rd_kafka_set_log_level(handler_, 1);

	/* Add brokers */
    if (rd_kafka_brokers_add(handler_, brokers) == 0)
    {
        fprintf(stderr, "****** No valid brokers specified********\n");
 		return PRODUCER_INIT_FAILED;       
    }	
	

	/* Create topic */
    topic_ = rd_kafka_topic_new(handler_, topic, topic_conf_);
	
	return PRODUCER_INIT_SUCCESS;
}

void ProducerKafka::destroy()
{
	/* Destroy topic */
    rd_kafka_topic_destroy(topic_);

    /* Destroy the handle */
    rd_kafka_destroy(handler_);
}

int ProducerKafka::push_data_to_kafka(const char* buffer, const int buf_len)
{
	int ret;
	char errstr[512]={0};
	
	if(NULL == buffer)
		return 0;

	ret = rd_kafka_produce(topic_, partition_, RD_KAFKA_MSG_F_COPY, 
							(void*)buffer, (size_t)buf_len, NULL, 0, NULL);

	if(ret == -1)
	{
		fprintf(stderr,"****Failed to produce to topic %s partition %i: %s*****\n",
			rd_kafka_topic_name(topic_), partition_,
			rd_kafka_err2str(rd_kafka_errno2err(errno)));
	
		rd_kafka_poll(handler_, 0);
		return PUSH_DATA_FAILED;
	}
	
	fprintf(stderr, "***Sent %d bytes to topic:%s partition:%i*****\n",
		buf_len, rd_kafka_topic_name(topic_), partition_);

	rd_kafka_poll(handler_, 0);

	return PUSH_DATA_SUCCESS;
}


TEST(QueueKafkaTest, Basic){
        char test_data[100];
        ProducerKafka* producer = new ProducerKafka;
        if (PRODUCER_INIT_SUCCESS == producer->init_kafka(0,"10.25.231.195:9092","kafka_newsparser_algo_1005")){
                printf("producer init success\n");
        }else{
                printf("produce init failed\n");
                assert(1);
                //return 0;
        }


        base_logic::DictionaryValue* task_info = new base_logic::DictionaryValue();
  /*{"id":560, "attrid":14, "depth":3, "cur_depth":2, "method":2, "url":"http://tech.caijing.com.cn/index.html"}
   */
        int re = PUSH_DATA_SUCCESS;
        task_info->Set(L"id", base_logic::Value::CreateBigIntegerValue(10));
        task_info->Set(L"attrid", base_logic::Value::CreateBigIntegerValue(4));
        task_info->Set(L"depth", base_logic::Value::CreateIntegerValue(2));
        task_info->Set(L"cur_depth",
                 base_logic::Value::CreateIntegerValue(0));
        task_info->Set(L"method", base_logic::Value::CreateIntegerValue(4));
        task_info->Set(L"machine", base_logic::Value::CreateIntegerValue(2));
        task_info->Set(L"storage", base_logic::Value::CreateIntegerValue(1));
        task_info->Set(L"is_login", base_logic::Value::CreateIntegerValue(0));
        task_info->Set(L"is_over", base_logic::Value::CreateIntegerValue(1));
        task_info->Set(L"polling_time",
                 base_logic::Value::CreateBigIntegerValue(141412123));
        task_info->Set(L"last_time",
                 base_logic::Value::CreateBigIntegerValue(242421));
        task_info->Set(L"url", base_logic::Value::CreateStringValue("https://market.console.aliyun.com"));
        std::string json_str;
        base_logic::ValueSerializer* engine = base_logic::ValueSerializer::Create(0, &json_str);
        base_logic::Value* data = (base_logic::Value*)(task_info);
        engine->Serialize(*data);
        //printf("[%d][%s]",json_str.length(),json_str.c_str());
        size_t len = strlen(test_data);
        if (test_data[len - 1] == '\n')
                test_data[--len] = '\0';
	if (PUSH_DATA_SUCCESS == producer->push_data_to_kafka(json_str.c_str(), json_str.length()))
                printf("push data success %s\n", json_str.c_str());
        else
                printf("push data failed %s\n", json_str.c_str());
        char test_data1[]="ttttttyyyyyy";
	/*while (fgets(test_data, sizeof(test_data), stdin)) {
		size_t len = strlen(test_data);
		if (test_data[len - 1] == '\n')
			test_data[--len] = '\0';
		if (strcmp(test_data, "end") == 0)
			break;
		if (PUSH_DATA_SUCCESS == producer->push_data_to_kafka(test_data1, strlen(test_data1)))
			printf("push data success %s\n", test_data1);
		else
			printf("push data failed %s\n", test_data1);
	}*/
        sleep(10);
	producer->destroy();
	
	//return 0;	
}
