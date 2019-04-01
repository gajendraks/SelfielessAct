var link="http://localhost:5000";
var incr = (function () {
    var a_id = 1;

    return function () {
        return a_id++;
    }
})();



function SHA1 (msg) {
    function rotate_left(n,s) {
        var t4 = ( n<<s ) | (n>>>(32-s));
        return t4;
    };
    function lsb_hex(val) {
        var str="";
        var i;
        var vh;
        var vl;
        for( i=0; i<=6; i+=2 ) {
            vh = (val>>>(i*4+4))&0x0f;
            vl = (val>>>(i*4))&0x0f;
            str += vh.toString(16) + vl.toString(16);
        }
        return str;
    };
    function cvt_hex(val) {
        var str="";
        var i;
        var v;
        for( i=7; i>=0; i-- ) {
            v = (val>>>(i*4))&0x0f;
            str += v.toString(16);
        }
        return str;
    };
    function Utf8Encode(string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
        }
        return utftext;
    };
    var blockstart;
    var i, j;
    var W = new Array(80);
    var H0 = 0x67452301;
    var H1 = 0xEFCDAB89;
    var H2 = 0x98BADCFE;
    var H3 = 0x10325476;
    var H4 = 0xC3D2E1F0;
    var A, B, C, D, E;
    var temp;
    msg = Utf8Encode(msg);
    var msg_len = msg.length;
    var word_array = new Array();
    for( i=0; i<msg_len-3; i+=4 ) {
        j = msg.charCodeAt(i)<<24 | msg.charCodeAt(i+1)<<16 |
        msg.charCodeAt(i+2)<<8 | msg.charCodeAt(i+3);
        word_array.push( j );
    }
    switch( msg_len % 4 ) {
        case 0:
            i = 0x080000000;
        break;
        case 1:
            i = msg.charCodeAt(msg_len-1)<<24 | 0x0800000;
        break;
        case 2:
            i = msg.charCodeAt(msg_len-2)<<24 | msg.charCodeAt(msg_len-1)<<16 | 0x08000;
        break;
        case 3:
            i = msg.charCodeAt(msg_len-3)<<24 | msg.charCodeAt(msg_len-2)<<16 | msg.charCodeAt(msg_len-1)<<8    | 0x80;
        break;
    }
    word_array.push( i );
    while( (word_array.length % 16) != 14 ) word_array.push( 0 );
    word_array.push( msg_len>>>29 );
    word_array.push( (msg_len<<3)&0x0ffffffff );

    for ( blockstart=0; blockstart<word_array.length; blockstart+=16 ) {
        for( i=0; i<16; i++ ) W[i] = word_array[blockstart+i];
        for( i=16; i<=79; i++ ) W[i] = rotate_left(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1);
        A = H0;
        B = H1;
        C = H2;
        D = H3;
        E = H4;
        for( i= 0; i<=19; i++ ) {
            temp = (rotate_left(A,5) + ((B&C) | (~B&D)) + E + W[i] + 0x5A827999) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
        for( i=20; i<=39; i++ ) {
            temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
        for( i=40; i<=59; i++ ) {
            temp = (rotate_left(A,5) + ((B&C) | (B&D) | (C&D)) + E + W[i] + 0x8F1BBCDC) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
        for( i=60; i<=79; i++ ) {
            temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
        H0 = (H0 + A) & 0x0ffffffff;
        H1 = (H1 + B) & 0x0ffffffff;
        H2 = (H2 + C) & 0x0ffffffff;
        H3 = (H3 + D) & 0x0ffffffff;
        H4 = (H4 + E) & 0x0ffffffff;
    }
    var temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4);
    return temp.toLowerCase();
}



  function register()
  {
    var username=document.getElementById('reg_username').value;
    var password=document.getElementById('reg_pwd').value;
    var url=link+"/api/v1/users";

    var encrypted=SHA1(password);
    console.log(encrypted)


    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
      if (this.readyState==4){
        console.log(this.status);
        //var json = JSON.parse(xhttp.responseText);
        //console.log(json);
        if (this.status==201)
        { 
          var success=document.getElementById('success');
          success.innerHTML="Operation Success";
          success.style.display="block";
        }else{
        var success=document.getElementById('success');
        success.innerHTML="Operation Failure";
        success.style.display="block";
      }

      }
      
    };
    xhttp.open("POST",url,true);
    xhttp.setRequestHeader("Content-Type","application/json");
    var data=JSON.stringify({"username":username,"password":encrypted});
    console.log(data);
    xhttp.send(data);
  }


  function delete_user()
  {
      var username = document.getElementById("del_username").value;
      var url = link+"/api/v1/users/"+username
    
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
          if(this.readyState==4){
              console.log(this.status);

              if (this.status==200)
              {
                  var success = document.getElementById('success');
                  success.innerHTML="Operation Successful";
                  success.style.display="block";
              }
              else
              {
                var success = document.getElementById('success');
                success.innerHTML="Operation Not Successful";
                success.style.display="block";
              }
          }
      };
      
      xhttp.open("DELETE",url,true);
      xhttp.send();
  }

  function add_category()
  {
      var cat_name = document.getElementById("category_name").value;
      var url = link+"/api/v1/categories"

      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
          if(this.readyState==4){
              console.log(this.status);
            //   var json = JSON.parse(xhttp.responseText);
            //   console.log(json);

              if (this.status==201)
              {
                  var success = document.getElementById('add_cat_success');
                  success.innerHTML="Operation Successful";
                  success.style.display="block";
              }
              else
              {
                var success = document.getElementById('add_cat_success');
                success.innerHTML="Operation Not Successful";
                success.style.display="block";
              }
          }
    };
      
    xhttp.open("POST",url,true);
    xhttp.setRequestHeader("Content-Type","application/json");
    var data=JSON.stringify([cat_name]);
    console.log(data);
    xhttp.send(data);

  }

  function remove_category()
  {
      var cat_name = document.getElementById("remove_category_name").value;
      var url = link+"/api/v1/categories/"+cat_name;

      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
          if(this.readyState==4){
              console.log(this.status);

              if (this.status==200)
              {
                  var success = document.getElementById('remove_cat_success');
                  success.innerHTML="Operation Successful";
                  success.style.display="block";
              }
              else
              {
                var success = document.getElementById('remove_cat_success');
                success.innerHTML="Operation Not Successful";
                success.style.display="block";
              }
          }
      };
      xhttp.open("DELETE",url,true);
      xhttp.send();
  }

  function list_categories()
  {
    var url = link+"/api/v1/categories";

    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
          if(this.readyState==4){
              console.log(this.status);

              if (this.status==200)
              {
                  var success = document.getElementById('list_cat');
                  success.innerHTML=this.responseText
                  success.style.display="block";
              }
              else
              {
                var success = document.getElementById('list_cat');
                success.innerHTML="Operation Not Successful";
                success.style.display="block";
              }
          }
      };
      xhttp.open("GET",url,true);
      xhttp.send();

  }

function list_acts()
{
    var category_name = document.getElementById("category_name").value;
    var start = document.getElementById("start").value;
    var end = document.getElementById("end").value;
    
    if(start == "" || end == ""){
    var url = link+"/api/v1/categories/"+category_name+"/acts";

    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
          if(this.readyState==4){
              console.log(this.status);

              if (this.status==204)
              {
                  var success = document.getElementById('list_acts_display');
                  success.innerHTML="No content"
                  success.style.display="block";
              }
              else if(this.status==413)
              {
                var success = document.getElementById('list_acts_display');
                success.innerHTML="Too large to display mor than 100";
                success.style.display="block";
              }
              else if(this.status==200)
              {
                var success = document.getElementById('list_acts_display');
                success.innerHTML=this.responseText;
                success.style.display="block";
              }
          }
      };
      xhttp.open("GET",url,true);
      xhttp.send();
    }
    else{
        var url=link+"/api/v1/categories/"+category_name+"/acts?start="+start+"&end="+end;

        var xhttp=new XMLHttpRequest();

		xhttp.onreadystatechange=function() {
	    	if (this.readyState==4){

	    		if(this.status==200)
		        {
		        	var success = document.getElementById('list_acts_display');
                    success.innerHTML=this.responseText;
                    success.style.display="block";


		        }
		        else if(this.status==204)
		        {

                    var success = document.getElementById('list_acts_display');
                    success.innerHTML="No content"
                    success.style.display="block";

		        }
		        else if(this.status==413)
		        {

		        	var success = document.getElementById('list_acts_display');
                    success.innerHTML="Too large to display mor than 100";
                    success.style.display="block";

		        }
		        else if(this.status==405)
		        {
                    var success = document.getElementById('list_acts_display');
                    success.innerHTML="Method not allowed";
                    success.style.display="block";
		        }

	    	}
	    };


		xhttp.open("GET",url,true);
	    xhttp.setRequestHeader("Content-Type","application/json");
	    var data=JSON.stringify({});
	    //console.log(data);
	    xhttp.send(data);
    }
}




function upload_acts()
	{

		var url=link+"/api/v1/acts";
		//var actId=document.getElementById("actid").value;
		var actId=incr();
		var username=document.getElementById("username").value;
		var timestamp=document.getElementById("timestamp").value;
		var caption=document.getElementById("caption").value;
		var categoryName=document.getElementById("categoryName").value;
		//var imgB64=document.getElementById("imgB64").value;
		var imgB64="bWF5byBvciBtdXN0Pw==";

        console.log(username);
		dict={
			"actId":parseInt(actId),
			"username":username,
			"timestamp":timestamp,
			"caption":caption,
			"categoryName":categoryName,
			"imgB64":imgB64
		}

        console.log(dict)

		var xhttp=new XMLHttpRequest();

		xhttp.onreadystatechange=function() {
	    	if (this.readyState==4){

	    		if(this.status==201)
		        {	
		        	console.log(this.status);
		        	console.log("UPLOADED");
		        	var success=document.getElementById('upload_success');
		        	success.innerHTML="Successfully uploaded";
		        	success.style.display="block";
		        	success.style.position="relative";
		        	success.style.left="40vh";
		        }
		        else
		        {
		        	console.log(this.status);
		        	console.log("UPLOADED");
		        	var success=document.getElementById('upload_success');
		        	success.innerHTML="Upload UnSuccessful";
		        	success.style.display="block";
		        	success.style.position="relative";
		        	success.style.left="40vh";
		        }
	    	}
	    };

		xhttp.open("POST",url,true);
	    xhttp.setRequestHeader("Content-Type","application/json");
	    var data=JSON.stringify(dict);
	    //console.log(data);
	    xhttp.send(data);		


	}


function upvote_act(){
    var url=link+"/api/v1/acts/upvote";
        var actId = document.getElementById("upvote_act").value;
		console.log(actId,typeof actId);
        // actId = parseInt(actId);
		var xhttp=new XMLHttpRequest();

		xhttp.onreadystatechange=function() {
	    	if (this.readyState==4){

	    		if(this.status==200)
		        {	
		        	console.log(this.status);
		        	console.log("UPVOTED");	
		        }
	    	}
	    };

		xhttp.open("POST",url,true);
	    xhttp.setRequestHeader("Content-Type","application/json");
	    var data=JSON.stringify([parseInt(actId)]);
	    //console.log(data);
	    xhttp.send(data);
}


function remove_act() {
    
    var actId = document.getElementById("remove_act").value;
    // parseInt(actId) 
    console.log(actId,typeof actId);
    var url=link+"/api/v1/acts/"+actId;

    var xhttp=new XMLHttpRequest();

    xhttp.onreadystatechange=function() {
        if (this.readyState==4){

            if(this.status==200)
            {	
                console.log(this.status);
                console.log("REMOVED");	
            }
        }
    };

    xhttp.open("DELETE",url,true);
    xhttp.setRequestHeader("Content-Type","application/json");
    var data=JSON.stringify({});
    //console.log(data);
    xhttp.send(data);		

}