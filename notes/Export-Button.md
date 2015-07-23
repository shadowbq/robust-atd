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

