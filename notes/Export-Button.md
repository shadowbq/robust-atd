EXTJS Export Request:

```js
exportResults : function(e, target, options){
		columns="";
		var i=0;
		Ext.getCmp("AnalysisResultsGridBox").headerCt.getMenu().items.last().menu.items.each(function(item){
			item.checked== true?(columns=columns+":"+item.text):0;
		});		
			
		var hiddenForm = Ext.create('Ext.form.Panel', {
		  title:'hiddenForm',
		  standardSubmit: true,
		  timeout: 240000,
		  height:0,
		  width: 0,
		  hidden:true,
		  headers : {
				'Accept' : 'application/vnd.ve.v1.0+json',
				'Content-Type' : 'application/json',
				'VE-SDK-API' : Base64.encode(ValidEdge.utils.SingletonSession.session + ":" + ValidEdge.utils.SingletonSession.userId)
			}
		})
		hiddenForm.getForm().submit({
			url : '/php/configloader/getremoteExportReport.php?page=resultspage&userid='+ValidEdge.utils.SingletonSession.userId+'&host='+options.host+'&columns='+columns,
		    method: 'POST',
			standardSubmit:true,
			target: '_blank',
			isUpload: true,
			params:{
			  	postHeader : Base64.encode(ValidEdge.utils.SingletonSession.session + ":" + ValidEdge.utils.SingletonSession.userId)
				//columns : Ext.encode(columns),
			},
				
			  	scope : this
			})
		
	},
```	

Core Information:

```js
url : '/php/configloader/getremoteExportReport.php?page=resultspage&userid='+ValidEdge.utils.SingletonSession.userId+'&host='+options.host+'&columns='+columns,
method: 'POST'
```

columns possible (correctly formatted)
```
":Reports:Submitted Time:Severity:File Name:File Type:User:Job Id:Task Id:URL:Analyzer Profile:VM Profile:Hash:File Size:Source IP:Destination IP"
```

Additional Dump

```js
ValidEdge.utils.SingletonSession.userId
"1"

ValidEdge.utils.SingletonSession.session
"2qmdlsu1k4g8e61a9dks4u8p90
```
## General

```
Remote Address:50.134.25.194:443
Request URL:https://atd.localhost.com/php/configloader/getremoteExportReport.php?page=resultspage&userid=1&host=localhost&columns=:Reports:Submitted%20Time:Severity:File%20Name:File%20Type:User:URL:Analyzer%20Profile:VM%20Profile:Hash:File%20Size:Source%20IP:Destination%20IP
Request Method:POST
Status Code:200 OK
```

## Response Headers

```
Cache-Control:no-store, no-cache, must-revalidate, private,max-age=0
Connection:keep-alive
Content-Description:File Transfer
Content-Disposition:attachment; filename="results.csv"
Content-Length:2199
Content-Type:application/vnd.ms-excel
Date:Thu, 23 Jul 2015 03:53:08 GMT
Expires:Sat, 26 Jul 1997 05:00:00 GMT
Pragma:no-cache
Server:nginx/1.4.6 (Ubuntu)
X-Content-Type-Options:nosniff
```

## Request Headers

```
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:en-US,en;q=0.8
Cache-Control:no-cache
Connection:keep-alive
Content-Length:55
Content-Type:application/x-www-form-urlencoded
Cookie:PHPSESSID=pgojo3du16u15ol2t33umrdek2
DNT:1
Host:atd.localhost.com
Origin:https://atd.localhost.com
Pragma:no-cache
Referer:https://atd.localhost.com/matdindex.php
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
```

## Query String Parameters
```
page:resultspage
userid:1
host:localhost
columns::Reports:Submitted Time:Severity:File Name:File Type:User:URL:Analyzer Profile:VM Profile:Hash:File Size:Source IP:Destination IP
```

## Form Data
```
postHeader:cGdvam8zZHUxNnUxNW9sMnQzM3VtcmRlazI6MQ==
```
