# tde(trading data extractor)

---
a simple restful api server to retrieve XRPUSDT trading data
- python 2.7


### api

- `/api/status`  
get server status
  - return type: str
  - return content: `ok: timemark`
- `/api/trade/xrpusdt/(?P<start_time>\d{13})...(?P<end_time>\d{13})`  
retrieve XRPUSDT trading data by start and end timestamp
  - return type: json
  - return json structure: `{"msg": None, "code": 0, "data": None or {"total": 0, "items": []}}`
    - item structure: `[id, timestamp, price, quantity, side]`

### deploy
1. before deploy, using `init_script` to setup the db file
1. ensure linux and python2.7 with virtualenv environment ok
2. `supervisor` is a good choice to manage the server process

### time complexity
`n` is total of dataset  
`m` is result length  
there are two ways i've tried:
1. plain python AVLTree
    1. building avltree on each startup: time complexity is `O(log n!)`, took about 460s on my i5 mac air, if the original data is already sorted by timestamp, this step can be `O(n)`
    2. query data: `O(log n) + O(log n) + O(m)` thus `O(log n)` 
2. sqlite database
    1. build database(data + index): `O(n) + O(log n!)`
    2. query data: `O(log n)`

pure python avl-tree is slower than sqlite even they have same time complexity level. because the limitation of Python.

### performance
- machine: MacBook Air (13-inch, Early 2015)  
- cpu: 1.6 GHz Intel Core i5  
- memory: 8 GB 1600 MHz DDR3  
- hard drive: 128G ssd
1. avltree(`TreeQueryHandler`) / json / 1 process / 1 thread / no coroutine / no cache:
    ```
    Server Software:        TornadoServer/4.5.3
    Server Hostname:        localhost
    Server Port:            8888
    
    Document Path: /api/trade/xrpusdt/1582517614209...1582519924699
    Document Length:        467490 bytes
    
    Concurrency Level:      100
    Time taken for tests:   40.906 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      467681000 bytes
    HTML transferred:       467490000 bytes
    Requests per second:    24.45 [#/sec] (mean)
    Time per request:       4090.641 [ms] (mean)
    Time per request:       40.906 [ms] (mean, across all concurrent requests)
    Transfer rate:          11164.99 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   1.5      0      15
    Processing:    34 3887 1517.2   3726   12635
    Waiting:       33 3860 1476.1   3724   12635
    Total:         40 3888 1517.4   3726   12642
    
    Percentage of the requests served within a certain time (ms)
      50%   3726
      66%   3846
      75%   3949
      80%   4095
      90%   4588
      95%   4776
      98%  11891
      99%  12281
     100%  12642 (longest request)
    ```
2. sqlite(`DBQueryHandler`) / json / 1 process / 1 thread / no coroutine / no cache:
    ```
    Server Software:        TornadoServer/4.5.3
    Server Hostname:        localhost
    Server Port:            8888
    
    Document Path:          /api/trade/xrpusdt/1582517614209...1582519924699
    Document Length:        57281 bytes
    
    Concurrency Level:      100
    Time taken for tests:   5.363 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      57471000 bytes
    HTML transferred:       57281000 bytes
    Requests per second:    186.47 [#/sec] (mean)
    Time per request:       536.271 [ms] (mean)
    Time per request:       5.363 [ms] (mean, across all concurrent requests)
    Transfer rate:          10465.60 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   1.2      0       7
    Processing:     8  505 148.5    527    1380
    Waiting:        8  505 148.5    527    1380
    Total:         13  506 148.5    528    1385
    
    Percentage of the requests served within a certain time (ms)
      50%    528
      66%    534
      75%    535
      80%    537
      90%    546
      95%    555
      98%    558
      99%   1343
     100%   1385 (longest request)
    ```
3. sqlite(`DBQueryHandler`) / ujson / 4 process / 1 thread per process / no coroutine / no cache:
    ```
    Server Software:        TornadoServer/4.5.3
    Server Hostname:        localhost
    Server Port:            8888
    
    Document Path:          /api/trade/xrpusdt/1582517614209...1582519924699
    Document Length:        50574 bytes
    
    Concurrency Level:      100
    Time taken for tests:   2.073 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      50764000 bytes
    HTML transferred:       50574000 bytes
    Requests per second:    482.28 [#/sec] (mean)
    Time per request:       207.347 [ms] (mean)
    Time per request:       2.073 [ms] (mean, across all concurrent requests)
    Transfer rate:          23908.82 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    2   4.4      0      20
    Processing:     8  196  54.4    195    1271
    Waiting:        4  195  54.5    195    1271
    Total:          8  197  51.9    195    1273
    
    Percentage of the requests served within a certain time (ms)
      50%    195
      66%    204
      75%    211
      80%    217
      90%    237
      95%    254
      98%    272
      99%    274
     100%   1273 (longest request)
    ```
4. situation 3 with cache:
    ```
    Server Software:        TornadoServer/4.5.3
    Server Hostname:        localhost
    Server Port:            8888
    
    Document Path:          /api/trade/xrpusdt/1582517614209...1582519924699
    Document Length:        50574 bytes
    
    Concurrency Level:      100
    Time taken for tests:   0.604 seconds
    Complete requests:      1000
    Failed requests:        996
       (Connect: 0, Receive: 0, Length: 996, Exceptions: 0)
    Total transferred:      396280 bytes
    HTML transferred:       202296 bytes
    Requests per second:    1655.55 [#/sec] (mean)
    Time per request:       60.403 [ms] (mean)
    Time per request:       0.604 [ms] (mean, across all concurrent requests)
    Transfer rate:          640.68 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   2.7      0      24
    Processing:     5   56  57.4     45     467
    Waiting:        5   54  57.6     44     467
    Total:         10   57  58.4     46     473
    
    Percentage of the requests served within a certain time (ms)
      50%     46
      66%     50
      75%     52
      80%     52
      90%     88
      95%     93
      98%    329
      99%    467
     100%    473 (longest request)
    ```
#### explanation
- Python avl tree took a lot of time to initiate on each startup (this can be improved by saving the built tree to disk)
- all ab test are using one url, to prevent ~100% cache hit, cache was disabled in 3/4 situations.
- comparing 1 and 2 we can see that pure python avl tree used about 40s to finish the test while sqlite used less than 6s. this doesn't mean pure Python is so bad on this. but because sqlite has internal improvements like cache.
- test 4 is an extremely situation while all requests have the same time range

### bottleneck
- request urls can be collected to analyze the query range's distribution, and find way to improve cache.
- large range query will take more time to extract the data and serialize it. we can set default limitation to prevent this kind of request blocking the server.
- cache i'm using now is on process level and this can be duplicate among processes. so consistent hash can be use to improve this situation. also we can improve this by adding gateway cache.
- the best way to identify the bottleneck is to do Stress Testing. which is to disable process cache and generate random time range queries. And we can observe the system stats like cpu/disk and network io/file descriptor during the test.
- this project is just a simple case while we will face write and query in production. there would be much more problems and details to be solved.
- ...
