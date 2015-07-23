To Request a JSON data set of results 

## General
```
Remote Address:50.134.25.194:443
Request URL:https://atd.localhost.com/php/configloader/getremotesamplestatus.php?userid=1&status=5&showAll=0&time=0&showAll=0&host=localhost&page=1&start=0&limit=20&sort=%5B%7B%22property%22%3A%22severity%22%2C%22direction%22%3A%22DESC%22%7D%5D
Request Method:GET
Status Code:200 OK
```

## Request Headers
```
Accept:application/vnd.ve.v1.0+json
Accept-Encoding:gzip, deflate, sdch
Accept-Language:en-US,en;q=0.8
Cache-Control:no-cache
Connection:keep-alive
Content-Type:application/json
Cookie:PHPSESSID=2qmdlsu1k4g8e61a9dks4u8p90
DNT:1
Host:atd.localhost.com
Pragma:no-cache
Referer:https://atd.localhost.com/matdindex.php
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
VE-SDK-API:MnFtZGxzdTFrNGc4ZTYxYTlka3M0dThwOTA6MQ==
X-Requested-With:XMLHttpRequest
```
```js
VE-SDK-API: Base64.encode(ValidEdge.utils.SingletonSession.session + ":" + ValidEdge.utils.SingletonSession.userId)
```
## Query String Parameters
```
userid:1
status:5
showAll:0
time:0
showAll:0
host:localhost
page:2
start:20
limit:20
sort:[{"property":"severity","direction":"DESC"}]
```

### Show all

If you want all the submissions, regardless of severity, set showAll to 1.

```
&showAll=1
```

### Time restriction

The standard pull down does a time restriction in minutes from now.
```
// 1 Hour
time=60
// 30 Days
time=43200
```
If you want the entire DB.
```
time=0
```

### File Restriction

This returns the last X files submitted. Use of `files` is instead of `time`.

```
files:10
```
