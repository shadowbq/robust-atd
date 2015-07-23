# Export Button

The export button is state tracked by the users previous request. This request must follow a analysis results query.

## EXTJS Export Request:

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

## BUG present in column selector.
* One common factor is that the first column is omitted from the export
* Second is that if Submittied Time is not the second column.. all hell breaks loose on the parser.

This is a useful export.
```
":Reports:Submitted Time:Severity:Job Id:Task Id:Analyzer Profile:Hash"
```

It actually only exports 
```
:Submitted Time:Severity:Job Id: Task If: Analyzer:Hash:
```

```
"Submitted Time",Severity,"Job Id","Task Id","Analyzer Profile",Hash
"2015-07-22 15:54:21","Very High",21424,40048,"Win XP Down Select (Online)",5573641A9E543C104E9D58FD6AFA141D
"2015-07-22 15:52:25","Very High",21417,40041,"Windows XP Full Run Online",5AA7BC2A4A3CA85F127D8678400028A5
"2015-07-19 17:44:11","Very High",21121,39745,"Windows 7 64bit Down Select (Online)",C702A1441672050B54D1565970FACADE
"2015-07-19 17:44:01","Very High",21119,39743,"Windows 7 64bit Down Select (Online)",C702A1441672050B54D1565970FACADE
"2015-07-19 17:43:57","Very High",21117,39741,"Windows 7 64bit Down Select (Online)",C702A1441672050B54D1565970FACADE
"2015-07-19 17:43:47","Very High",21114,39738,"Windows 7 64bit Down Select (Online)",C702A1441672050B54D1565970FACADE
"2015-07-17 14:47:18","Very High",20750,39374,"Windows 7 64bit Down Select (Online)",9FE1F8407E73F02EC10FCE2EA64A4795
"2015-07-17 13:30:02","Very High",20741,39365,"Windows 7 64bit Down Select (Online)",8E5F7F607ECAFA454A3ACA35B048A8EA
"2015-07-16 09:43:45","Very High",20589,39213,"Windows 7 64bit Down Select (Online)",502DFDB990CFB62F56461EA5A077F043
"2015-07-16 00:18:35","Very High",20585,39209,"Windows 7 64bit Down Select (Online)",950ACE1259DF56330759312A57ACC2E5
"2015-07-15 13:50:33","Very High",20506,39130,"Windows 7 64bit Down Select (Online)",9A669FF30D7CAF9A70C524790E0AE8E4
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
