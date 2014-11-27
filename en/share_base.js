
function $$(ele) {
	return typeof ele == 'string' ? document.getElementById(ele) : ele;
}

function disableTextField (field) {
	if (document.all || document.getElementById)
		field.disabled = true;
	else {
		field.oldOnFocus = field.onfocus;
		field.onfocus = skip;
	}
}
function enableTextField (field) {
	if (document.all || document.getElementById)
		field.disabled = false;
	else {
		field.onfocus = field.oldOnFocus;
	}
}
///ql_xu add
function Lan1NeqLan2(ip1, mask1, ip2, mask2)
{
	d11 = getDigit(ip1.value,1);
	d12 = getDigit(mask1.value, 1);
	d21 = getDigit(ip2.value,1);
	d22 = getDigit(mask2.value,1);
	d1 = d11 & d12;
	d2 = d21 & d22;
	if (d1 != d2)
		return true;
	
	d11 = getDigit(ip1.value,2);
	d12 = getDigit(mask1.value, 2);
	d21 = getDigit(ip2.value,2);
	d22 = getDigit(mask2.value,2);
	d1 = d11 & d12;
	d2 = d21 & d22;
	if (d1 != d2)
		return true;

	d11 = getDigit(ip1.value,3);
	d12 = getDigit(mask1.value, 3);
	d21 = getDigit(ip2.value,3);
	d22 = getDigit(mask2.value,3);
	d1 = d11 & d12;
	d2 = d21 & d22;
	if (d1 != d2)
		return true;

	d11 = getDigit(ip1.value,4);
	d12 = getDigit(mask1.value, 4);
	d21 = getDigit(ip2.value,4);
	d22 = getDigit(mask2.value,4);
	d1 = d11 & d12;
	d2 = d21 & d22;
	if (d1 != d2)
		return true;

	return false;
}

function disableRadioGroup (radioArrOrButton)
{
  if (radioArrOrButton.type && radioArrOrButton.type == "radio") {
        var radioButton = radioArrOrButton;
        var radioArray = radioButton.form[radioButton.name];
  }
  else
        var radioArray = radioArrOrButton;
        radioArray.disabled = true;
        for (var b = 0; b < radioArray.length; b++) {
        if (radioArray[b].checked) {
                radioArray.checkedElement = radioArray[b];
                break;
        }
  }
  for (var b = 0; b < radioArray.length; b++) {
        radioArray[b].disabled = true;
        radioArray[b].checkedElement = radioArray.checkedElement;
  }
}

function enableRadioGroup (radioArrOrButton)
{
  if (radioArrOrButton.type && radioArrOrButton.type == "radio") {
        var radioButton = radioArrOrButton;
        var radioArray = radioButton.form[radioButton.name];
  }
  else
        var radioArray = radioArrOrButton;

  radioArray.disabled = false;
  radioArray.checkedElement = null;
  for (var b = 0; b < radioArray.length; b++) {
        radioArray[b].disabled = false;
        radioArray[b].checkedElement = null;
  }
}

function disableCheckBox (checkBox) {
  if (!checkBox.disabled) {
    checkBox.disabled = true;
    if (!document.all && !document.getElementById) {
      checkBox.storeChecked = checkBox.checked;
      checkBox.oldOnClick = checkBox.onclick;
      checkBox.onclick = preserve;
    }
  }
}

function enableCheckBox (checkBox)
{
  if (checkBox.disabled) {
    checkBox.disabled = false;
    if (!document.all && !document.getElementById)
      checkBox.onclick = checkBox.oldOnClick;
  }
}


function check_wps_enc(enc, radius, auth)
{
        if (enc == 0 || enc == 1) {
                if (radius != 0)
                        return 2;
        }
        else {
                if (auth & 1)
                        return 2;
        }
        return 0;
}

function check_wps_wlanmode(mo, type)
{
        if (mo == 2) {
                return 1;
        }
        if (mo == 1 && type != 0) {
                return 1;
        }
        return 0;
}


function getDigit(str, num)
{
  i=1;
  if ( num != 1 ) {
  	while (i!=num && str.length!=0) {
		if ( str.charAt(0) == '.' ) {
			i++;
		}
		str = str.substring(1);
  	}
  	if ( i!=num )
  		return -1;
  }
  for (i=0; i<str.length; i++) {
  	if ( str.charAt(i) == '.' ) {
		str = str.substring(0, i);
		break;
	}
  }
  if ( str.length == 0)
  	return -1;
  d = parseInt(str, 10);
  return d;
}

function getDigitforMac(str, num)
{
  i=1;
  if ( num != 1 ) {
  	while (i!=num && str.length!=0) {
		if ( str.charAt(0) == '-' ) {
			i++;
		}
		str = str.substring(1);
  	}
  	if ( i!=num )
  		return -1;
  }
  for (i=0; i<str.length; i++) {
  	if ( str.charAt(i) == '-' ) {
		str = str.substring(0, i);
		break;
	}
  }
  if ( str.length == 0)
  	return -1;
  d = parseInt(str, 10);
  return d;
}

function validateKey(str)
{
   for (var i=0; i<str.length; i++) {
    if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') ||
    		(str.charAt(i) == '.' ) )
			continue;
	return 0;
  }
  return 1;
}

function validateDigit(str)
{
	if ((str.charAt(0) == '0') && ((str.charAt(1) == 'x') || (str.charAt(1) == 'X')))
	{//hex
		for (var i=2; i<str.length; i++)
		{
			if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') || 
				(str.charAt(i) >= 'A' && str.charAt(i) <= 'F')||
				(str.charAt(i) >= 'a' && str.charAt(i) <= 'f') )
				continue;
			return 0;
		}
	} else {//octet
		for (var i=2; i<str.length; i++)
		{
			if ( str.charAt(i) >= '0' && str.charAt(i) <= '9')
				continue;
			return 0;
		}
	}
	return 1;
}

function validateDecimalDigit(str)
{
	for (var i=0; i<str.length; i++)
	{
		if ( str.charAt(i) >= '0' && str.charAt(i) <= '9')
			continue;
		return 0;
	}
	return 1;
}

function getDigitFromString(str)
{
	var d;
	
	if ( str.length == 0)
		return -1;

	if ((str.charAt(0) == '0') && ((str.charAt(1) == 'x') || (str.charAt(1) == 'X')))
		d = parseInt(str, 16);
	else
		d = parseInt(str, 10);
	
	return d;
}


function validateKey2(str)
{
   for (var i=0; i<str.length; i++) {
    if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') ||
    		(str.charAt(i) == '-' ) || 
    		(str.charAt(i) >= 'A' && str.charAt(i) <= 'F')||
    		(str.charAt(i) >= 'a' && str.charAt(i) <= 'f') )
			continue;
	return 0;
  }
  return 1;
}

function IsLoopBackIP(str)
{
	d = getDigit(str,1);
	if(d==127)
		return 1;
	return 0;
}

function checkDigitRange(str, num, min, max)
{
  d = getDigit(str,num);
  if ( d > max || d < min )
      	return false;
  return true;
}

function checkDigitRangeforMac(str, num, min, max)
{  
  d = getDigitforMac(str,num);
  if ( d > max || d < min )
      	return false;
  return true;
}

function checkIP(ip)
{
	if (ip.value=="") {
		alert("IP address cannot be empty! It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
/*	if ( validateKey( ip.value ) == 0 ) {
		alert("Invalid IP address value. It should be the decimal number (0-9).");
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}*/
	//This is modified by wangrong at 2007-12-27
	var str=ip.value;
	var count=0;
	for (var i=0; i<str.length; i++) 
	{
		if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') )
			continue;
		if (str.charAt(i) == '.')
		{
			count++;
			continue;
		}
		alert("Invalid IP address value. It should be the decimal number (0-9).");
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if(count!=3)
	{
		alert("Invalid IP address. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx");
		ip.focus();
		return false;
	}
	
	if( IsLoopBackIP( ip.value)==1 ) {
		alert("Invalid IP address value.");
		ip.value = ip.defaultValue;	// Jenny,  Buglist B058, backward default value
		ip.focus();
		return false;
	}
	
	if ( !checkDigitRange(ip.value,1,1,223) ) {
		alert('Invalid IP address range in 1st digit. It should be 1-223.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,2,0,255) ) {
		alert('Invalid IP address range in 2nd digit. It should be 0-255.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,3,0,255) ) {
		alert('Invalid IP address range in 3rd digit. It should be 0-255.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,4,1,254) ) {
		alert('Invalid IP address range in 4th digit. It should be 1-254.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	
	return true;
}

function checkNotEmptyIP(ip)
{
	if (ip.value=="") {
		
		return true;
	}
/*	if ( validateKey( ip.value ) == 0 ) {
		alert("Invalid IP address value. It should be the decimal number (0-9).");
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}*/
	//This is modified by wangrong at 2007-12-27
	var str=ip.value;
	var count=0;
	for (var i=0; i<str.length; i++) 
	{
		if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') )
			continue;
		if (str.charAt(i) == '.')
		{
			count++;
			continue;
		}
		alert("Invalid IP address value. It should be the decimal number (0-9).");
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if(count!=3)
	{
		alert("Invalid IP address. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		ip.focus();
		return false;
	}
	
	if( IsLoopBackIP( ip.value)==1 ) {
		alert("Invalid IP address value.");
		ip.value = ip.defaultValue;	// Jenny,  Buglist B058, backward default value
		ip.focus();
		return false;
	}
	
	if ( !checkDigitRange(ip.value,1,1,223) ) {
		alert('Invalid IP address range in 1st digit. It should be 1-223.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,2,0,255) ) {
		alert('Invalid IP address range in 2nd digit. It should be 0-255.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,3,0,255) ) {
		alert('Invalid IP address range in 3rd digit. It should be 0-255.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	if ( !checkDigitRange(ip.value,4,1,254) ) {
		alert('Invalid IP address range in 4th digit. It should be 1-254.');
		ip.value = ip.defaultValue;
		ip.focus();
		return false;
	}
	
	return true;
}

//check if ip1 and ip2 is in the same network and ip1 is less ip2
function checkNetwork(ip1,ip2)
{
  ip_n = getDigit(ip1, 1);
  ip1_1 = getDigit(ip1,1);
  ip1_2 = getDigit(ip1,2);
  ip1_3 = getDigit(ip1,3);
  ip1_4 = getDigit(ip1,4);
  ip2_1 = getDigit(ip2,1);
  ip2_2 = getDigit(ip2,2);
  ip2_3 = getDigit(ip2,3);
  ip2_4 = getDigit(ip2,4);
  if(ip_n>=1 && ip_n<=126) 
  {
  	if(ip1_1 != ip2_1 || ip1_2>ip2_2 || (ip1_2==ip2_2 && ip1_3>ip2_3) ||(ip1_2==ip2_2 && ip1_3==ip2_3 && ip1_4>ip2_4))
  		return false;
  }
  else if(ip_n>=128 && ip_n<=191)
  {
  	if(ip1_1!=ip2_1 || ip1_2!=ip2_2 || ip1_3>ip2_3 || (ip1_3==ip2_3 && ip1_4>ip2_4))
  		return false;
  }
  else if(ip_n>=192 && ip_n<=223)
   {
  	if(ip1_1!=ip2_1 || ip1_2!=ip2_2 || ip1_3!=ip2_3 || ip1_4>ip2_4)
  		return false;
  }
  else
        return false;

  return true;
}

function checkMask(netmask)
{
 	 var str = new Array("", "1st", "2nd", "3rd", "4th");
	var i, d;
	var s,m;
	if (netmask.value=="") {
		alert("Subnet mask cannot be empty! It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		netmask.value = netmask.defaultValue;
		netmask.focus();
		return false;
	}
	
	/*if ( validateKey( netmask.value ) == 0 ) {
		alert("Invalid subnet mask value. It should be the decimal number (0-9).");
		netmask.value = netmask.defaultValue;
		netmask.focus();
		return false;
	}
	
	for (i=1; i<=4; i++) {
		d = getDigit(netmask.value,i);
		if( !(d==0 || d==128 || d==192 || d==224 || d==240 || d==248 || d==252 || d==254 || d==255 )) {
			alert('Invalid subnet mask '+str[i]+' digit.\nIt should be the number of 0, 128, 192, 224, 240, 248, 252 or 254');
			netmask.focus();
			return false;
		}
	}
	*/
	//This is modified by wangrong at 2007-12-27
	var str2=netmask.value;
	var count=0;
	for (i=0; i<str2.length; i++) 
	{
		if ( (str2.charAt(i) >= '0' && str2.charAt(i) <= '9')  )
			continue;
		if (str2.charAt(i) == '.')
		{
			count++;
			continue;
		}
		alert("Invalid  netmask value. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
			netmask.focus();
			return false;
		}
	if(count!=3)
	{
		alert("Invalid netmask value. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		netmask.focus();
		return false;
	}
	
	for (i=1; i<=4; i++) 
	{
		d = getDigit(netmask.value,i);		
		if( !(d==0 || d==128 || d==192 || d==224 || d==240 || d==248 || d==252 || d==254 || d==255 )) {
			alert('Invalid subnet mask '+str[i]+' digit.\nIt should be the number of 0, 128, 192, 224, 240, 248, 252 or 254');
			netmask.focus();
			return false;
		}
		if(d!=255)
		{	
			for(m=i+1;m<=4;m++)
			{
				s=getDigit(netmask.value,m);
				if(s!=0)
				{
					alert('Invalid subnet mask!');
					netmask.focus();
					return false;
				}
			}
			return true;
		}
		
	}
	return true;
}

/*alex_huang add 20090720  for netmask check 0.0.0.0 and 255.255.255.255*/
function checkMaskSpecial(netmask) /*check Mask 0.0.0.0 and 255.255.255.255*/
{
	 var str = new Array("", "1st", "2nd", "3rd", "4th");
	 var str2=netmask.value;
	 var i, d;
	  var s,m;
	  var count=0;
	  var d1,d2,d3,d4;
	  if (netmask.value=="") {
		alert("Subnet mask cannot be empty! It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		netmask.value = netmask.defaultValue;
		netmask.focus();
		return false;
	}
	for (i=0; i<str2.length; i++) 
	{
		if ( (str2.charAt(i) >= '0' && str2.charAt(i) <= '9')  )
			continue;
		if (str2.charAt(i) == '.')
		{
			count++;
			continue;
		}
		alert("Invalid  netmask value. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
			netmask.focus();
			return false;
		}
	if(count!=3)
	{
		alert("Invalid netmask value. It should be filled with 4 digit numbers as xxx.xxx.xxx.xxx.");
		netmask.focus();
		return false;
	}

	d1 = getDigit(netmask.value,1);
	d2 = getDigit(netmask.value,2);
	d3 = getDigit(netmask.value,3);
	d4 = getDigit(netmask.value,4);
	if((d1==0)&&(d2==0)&&(d3==0)&&(d4==0))
	{	
		alert("Invalid  netmask value. It should not be 0.0.0.0.");
		netmask.focus();
		return false;
	}
	if((d1==255)&&(d2==255)&&(d3==255)&&(d4==255))
	{	
		alert("Invalid  netmask value. It should not be 255.255.255.255.");
		netmask.focus();
		return false;
	}
	
	for (i=1; i<=4; i++) 
	{
		d = getDigit(netmask.value,i);		
		if( !(d==0 || d==128 || d==192 || d==224 || d==240 || d==248 || d==252 || d==254 || d==255 )) {
			alert('Invalid subnet mask '+str[i]+' digit.\nIt should be the number of 0, 128, 192, 224, 240, 248, 252 or 254');
			netmask.focus();
			return false;
		}
		
		if(d!=255)
		{	
			for(m=i+1;m<=4;m++)
			{
				s=getDigit(netmask.value,m);
				if(s!=0)
				{
					alert('Invalid subnet mask!');
					netmask.focus();
					return false;
				}
			}
			return true;
		}
		
	}

	return true;
}
/*alex_huang end*/
function includeSpace(str)
{
  for (var i=0; i<str.length; i++) {
  	if ( str.charAt(i) == ' ' ) {
	  return true;
	}
  }
  return false;
}

function checkString(str)
{
	for (var i=0; i<str.length; i++) {
		if ((str.charAt(i) >= '0' && str.charAt(i) <= '9') || (str.charAt(i) >= 'A' && str.charAt(i) <= 'Z') || (str.charAt(i) >= 'a' && str.charAt(i) <= 'z') ||
		   (str.charAt(i) == '.') || (str.charAt(i) == ':') || (str.charAt(i) == '-') || (str.charAt(i) == '_') || (str.charAt(i) == ' ') || (str.charAt(i) == '/') || (str.charAt(i) == '@'))
			continue;
		return 0;
	}
	return 1;
}

function deleteClick()
{
	if ( !confirm('Do you really want to delete the selected entry?') ) {
		return false;
	}
	else
		return true;
}
        
function deleteAllClick()
{
	if ( !confirm('Do you really want to delete the all entries?') ) {
		return false;
	}
	else
		return true;
}

function delClick(index)
{
	if ( !confirm('Are you sure you want to delete?') ) {
		return false;
	}
	
	document.actionForm.action.value=0;
	document.actionForm.idx.value=index;
	document.actionForm.submit();
	return true;
}


function delClick2(index,connid)
{
	if ( !confirm('Are you sure you want to delete?') ) {
		return false;
	}
	
	document.actionForm.action.value=0;
	document.actionForm.idx.value=index;
	document.actionForm.connid.value=connid; 
	document.actionForm.submit();
	return true;
}


function editClick(index)
{
	document.actionForm.action.value=1;
	document.actionForm.idx.value=index;
	document.actionForm.submit();
	return true;
}
function editClick2(index, connid)
{
     document.actionForm.action.value=1;
     document.actionForm.idx.value=index;
     document.actionForm.connid.value=connid; 
     document.actionForm.submit();
     return true;

}

function verifyBrowser() {
	var ms = navigator.appVersion.indexOf("MSIE");
	ie4 = (ms>0) && (parseInt(navigator.appVersion.substring(ms+5, ms+6)) >= 4);
	var ns = navigator.appName.indexOf("Netscape");
	ns= (ns>=0) && (parseInt(navigator.appVersion.substring(0,1))>=4);
	if (ie4)
		return "ie4";
	else
		if(ns)
			return "ns";
		else
			return false;
}

function isBrowser(b,v) {
	browserOk = false;
	versionOk = false;
	
	browserOk = (navigator.appName.indexOf(b) != -1);
	if (v == 0) versionOk = true;
	else  versionOk = (v <= parseInt(navigator.appVersion));
	return browserOk && versionOk;
}

function disableButton (button) {
  if (document.all || document.getElementById)
    button.disabled = true;
  else if (button) {
    button.oldOnClick = button.onclick;
    button.onclick = null;
    button.oldValue = button.value;
    button.value = 'DISABLED';
  }
}

function disableButtonIB (button) {
	if (isBrowser('Netscape', 0))
	{
		button.disabled = true;
		return;
	}
	if (document.all || document.getElementById)
		button.disabled = true;
	else if (button) {
		button.oldOnClick = button.onclick;
		button.onclick = null;
		button.oldValue = button.value;
		button.value = 'DISABLED';
	}
}

function disableButtonVB (button) {
  if (verifyBrowser() == "ns")
  	return;
  if (document.all || document.getElementById)
    button.disabled = true;
  else if (button) {
    button.oldOnClick = button.onclick;
    button.onclick = null;
    button.oldValue = button.value;
    button.value = 'DISABLED';
  }
}

function enableButton (button) {
  if (document.all || document.getElementById)
    button.disabled = false;
  else if (button) {
    button.onclick = button.oldOnClick;
    button.value = button.oldValue;
  }
}

function enableButtonVB (button) {
  if (verifyBrowser() == "ns")
  	return;
  if (document.all || document.getElementById)
    button.disabled = false;
  else if (button) {
    button.onclick = button.oldOnClick;
    button.value = button.oldValue;
  }
}

function enableButtonIB (button) {
	if (isBrowser('Netscape', 4))
	{	button.disabled = false;
		return;
	}
	if (document.all || document.getElementById)
		button.disabled = false;
	else if (button) {
		button.onclick = button.oldOnClick;
		button.value = button.oldValue;
	}
}

//This function is added by jim at 20090626
function checkFormatUnicastMac(macaddr)
{
	var str = macaddr.value;
	if ( str.length < 17)
	{
		alert("Input MAC address is not complete. Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}

	if(str == "00:00:00:00:00:00")
	{
	        alert("Invalid MAC address. MAC address can not be all '0'");
	        return false;
	 }
	var count=0;
	for (var i=0; i<str.length; i++) 
	{
		if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') ||
			(str.charAt(i) >= 'a' && str.charAt(i) <= 'f') ||
			(str.charAt(i) >= 'A' && str.charAt(i) <= 'F') )
			continue;
		if (str.charAt(i) == ':')
		{
			count++;
			continue;
		}
		alert("Invalid MAC address. It should be in hex number (0-9 or a-f). Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}
	
	if(count!=5)
	{
		alert("Invalid MAC address. It should be in hex number (0-9 or a-f). Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}
	if(str.charAt(1)&1)
	{
		alert("Broadcast/Multicast MAC is invalid!");
		macaddr.focus();
		return false;
	}
	return true;
}

//This function is added by wangrong at 2007-12-25
function checkMac(macaddr)
{
	var str = macaddr.value;
	if ( str.length < 17)
	{
		alert("Input MAC address is not complete. Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}

	if(str == "00:00:00:00:00:00")
	{
	        alert("Invalid MAC address. MAC address can not be all '0'");
		return false;
	}
	var count=0;
	for (var i=0; i<str.length; i++) 
	{
		if ( (str.charAt(i) >= '0' && str.charAt(i) <= '9') ||
			(str.charAt(i) >= 'a' && str.charAt(i) <= 'f') ||
			(str.charAt(i) >= 'A' && str.charAt(i) <= 'F') )
			continue;
		if (str.charAt(i) == ':')
		{
			count++;
			continue;
	}
		alert("Invalid MAC address. It should be in hex number (0-9 or a-f). Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}

	if(count!=5)
	{
		alert("Invalid MAC address. It should be in hex number (0-9 or a-f). Ex. xx:xx:xx:xx:xx:xx");
		macaddr.focus();
		return false;
	}
	return true;
}
//modified by ramen 20090605-exclude the broadcast&multicast
function checkMacWithoutColon(macAddr, checkEmpty)
{
	var i, macdigit = 0;

	if (checkEmpty == 1 && macAddr.value.length == 0) {
		//alert("MAC address cannot be empty");
		return false;
	}
	if(!checkEmpty&& macAddr.value.length == 0)
		return true;
	//tony 20111202 add: all zero mac is invalid
	var allZeroPattern = /^[0]{12}$/;
	if (allZeroPattern.exec(macAddr.value)) return false  ; 
	//tony 20111202 end
	var macPattern=/^[0-9a-fA-F]{1}[02468aAcCeE]{1}[0-9a-fA-F]{10}$/;
	if (!macPattern.exec(macAddr.value)) return false  ; 
	var broadcastpattern=/^[fF]{12}$/;
	if (broadcastpattern.exec(macAddr.value)) return false  ; 
	return true;
}
function routeClick(url)
{
	var wide=600;
	var high=400;
	if (document.all)
		var xMax = screen.width, yMax = screen.height;
	else if (document.layers)
		var xMax = window.outerWidth, yMax = window.outerHeight;
	else
	   var xMax = 640, yMax=480;
	var xOffset = (xMax - wide)/2;
	var yOffset = (yMax - high)/3;

	var settings = 'width='+wide+',height='+high+',screenX='+xOffset+',screenY='+yOffset+',top='+yOffset+',left='+xOffset+', resizable=yes, toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes';

	window.open( url, 'RouteTbl', settings );
}
//add by ramen
//type=1:at least one character
//type=0:may be empty
function checkSpecialChar(str,type)
{
		var patrn;
		if(type)
			patrn=/^[a-zA-Z0-9~`!@#$%^&*()_+|\\{}[\]:;<?,-./=']+$/; 
		else
			patrn=/^[a-zA-Z0-9~`!@#$%^&*()_+|\\{}[\]:;<?,-./=']*$/; 
		if (!patrn.exec(str)) return false  ; 
		if(str.indexOf("  ",0)!=-1)
			return false;
		return true;	
}
function checkEmail(str)
{
	var emailReg=/^([a-zA-Z0-9_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
	if (!emailReg.exec(str)) return false  ; 
	return true;
}

//star:20100825 IPV6_RELATED
function isIPv6(str)  
{  
return str.match(/:/g).length<=7  
&&/::/.test(str)  
?/^([\da-f]{1,4}(:|::)){1,6}[\da-f]{1,4}$/i.test(str)  
:/^([\da-f]{1,4}:){7}[\da-f]{1,4}$/i.test(str);  
} 
 
 function isNumber(value)
{
	return /^\d+$/.test(value);
}

function ParseIpv6Array(str)
{
    var Num;
    var i,j;
    var finalAddrArray = new Array();
    var falseAddrArray = new Array();
    
    var addrArray = str.split(':');
    Num = addrArray.length;
    if (Num > 8)
    {
        return falseAddrArray;
    }

    for (i = 0; i < Num; i++)
    {
        if ((addrArray[i].length > 4) 
            || (addrArray[i].length < 1))
        {
            return falseAddrArray;
        }
        for (j = 0; j < addrArray[i].length; j++)
        {
            if ((addrArray[i].charAt(j) < '0')
                || (addrArray[i].charAt(j) > 'f')
                || ((addrArray[i].charAt(j) > '9') && 
                (addrArray[i].charAt(j) < 'a')))
            {
                return falseAddrArray;
            }
        }

        finalAddrArray[i] = '';
        for (j = 0; j < (4 - addrArray[i].length); j++)
        {
            finalAddrArray[i] += '0';
        }
        finalAddrArray[i] += addrArray[i];
    }

    return finalAddrArray;
}

function getFullIpv6Address(address)
{
    var c = '';
    var i = 0, j = 0, k = 0, n = 0;
    var startAddress = new Array();
    var endAddress = new Array();
    var finalAddress = '';
    var startNum = 0;
    var endNum = 0;
    var lowerAddress;
    var totalNum = 0;

    lowerAddress = address.toLowerCase();
 
    var addrParts = lowerAddress.split('::');
    if (addrParts.length == 2)
    {
        if (addrParts[0] != '')
        {
            startAddress = ParseIpv6Array(addrParts[0]);
            if (startAddress.length == 0)
            {
                return '';
            }
        }
        if (addrParts[1] != '')
        {
            endAddress = ParseIpv6Array(addrParts[1]);
            if (endAddress.length == 0)
            {
               return '';
            }
        }

        if (startAddress.length +  endAddress.length >= 8)
        {
            return '';
        }
    }
    else if (addrParts.length == 1)
    {
        startAddress = ParseIpv6Array(addrParts[0]);
        if (startAddress.length != 8)
        {
            return '';
        }
    }
    else
    {
        return '';
    }

    for (i = 0; i < startAddress.length; i++)
    {
        finalAddress += startAddress[i];
        if (i != 7)
        {
            finalAddress += ':';
        }
    }
    for (; i < 8 - endAddress.length; i++)
    {
        finalAddress += '0000';
        if (i != 7)
        {
            finalAddress += ':';
        }
    }
    for (; i < 8; i++)
    {
        finalAddress += endAddress[i - (8 - endAddress.length)];
        if (i != 7)
        {
            finalAddress += ':';
        }
    }

    return finalAddress;
    
}

function isIpv6Address(address)
{
    if (getFullIpv6Address(address) == '')
    {
        return false;
    }
    
    return true;
}


function isUnicastIpv6Address(address)
{
    var tempAddress = getFullIpv6Address(address);
    
    if ((tempAddress == '')
        || (tempAddress == '0000:0000:0000:0000:0000:0000:0000:0000')
        || (tempAddress == '0000:0000:0000:0000:0000:0000:0000:0001')
        || (tempAddress.substring(0, 2) == 'ff'))
    {
        return false;
    }
    
    return true;
}

function isGlobalIpv6Address(address)
{
    var tempAddress = getFullIpv6Address(address);
    
    if ((tempAddress == '')
        || (tempAddress == '0000:0000:0000:0000:0000:0000:0000:0000')
        || (tempAddress == '0000:0000:0000:0000:0000:0000:0000:0001')
        || (tempAddress.substring(0, 3) == 'fe8')
        || (tempAddress.substring(0, 3) == 'fe9')
        || (tempAddress.substring(0, 3) == 'fea')
        || (tempAddress.substring(0, 3) == 'feb')
        || (tempAddress.substring(0, 2) == 'ff'))
    {
        return false;
    }
    
    return true;
}

function isLinkLocalIpv6Address(address)
{
    var tempAddress = getFullIpv6Address(address);
    
    if ( (tempAddress.substring(0, 3) == 'fe8')
        || (tempAddress.substring(0, 3) == 'fe9')
        || (tempAddress.substring(0, 3) == 'fea')
        || (tempAddress.substring(0, 3) == 'feb'))
    {
        return true;
    }
    
    return false;
}

function attentionDisplay(a) 
{		
	var attention = parent.document.getElementById('attention');
	if(a==1){
		attention.style.display="block";
	}else{
		attention.style.display="none";
	}
};
//star:20100825 IPV6_RELATED END

function checkSpecialCharForURL(str,type)
{		
	var patrn;		
	if(type)
		patrn=/^[a-zA-Z0-9~`!@$^*()_|\\{}[\]:;<,-.']+$/; 		
	else			
		patrn=/^[a-zA-Z0-9~`!@$^*()_|\\{}[\]:;<,-.']*$/; 		
	if (!patrn.exec(str)) 
		return false  ; 		
	if(str.indexOf("  ",0)!=-1)			
		return false;		
	return true;	
}

function checkSpecialCharExcludeSpace(str,type)
{		
	var patrn;
	if(type)
		patrn=/^[a-zA-Z0-9!#$%&()*+,-./:;=@[\]^_`{|}~<> ]+$/;
	else		
		patrn=/^[a-zA-Z0-9!#$%&()*+,-./:;=@[\]^_`{|}~<> ]*$/;
	if (!patrn.exec(str)) 
		return false  ; 				
	if(str.indexOf("  ",0)!=-1)			
		return false;		
	if(str.indexOf(" ",0)==0 || str.lastIndexOf(" ")==(str.length-1))		
	{			
		return false;		
	}			
	return true;
}