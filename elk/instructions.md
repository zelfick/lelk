# Prerequisites
docker installed and docker compose depending on your os would be different.

# Start the ekl stack
docker compose -f dockercompose.ekl.yaml up

# Verify services (3 containers elasticsearch, logstash and kibana)
docker container ps -fea

# Verify Elasticsearch is working correctly
curl http://localhost:9200

# Verify you can connect to Kibana and check indexes (Console) in the browser go to: http://localhost:5601
In the left pannel go to: ```Management -> Stack Management -> Index Management``` , and verify the index was created correctly

Then you can go to: ```Management -> Devtools``` to create and execute some queries:

```
GET /_cat/indices

GET testlog-logstash/_search
{
    "query": {
        "matc_all": {}
    }
}
```
# Enable searches and dashoboard
Go to: ```Management -> Kibana -> IndexPatterns```
Add there the nginx index or whatever other you have configured. 
Then you can go to: Analitics -> Discover
There you would have your nginx logs visible then you can filter and create queries as well visualizations
