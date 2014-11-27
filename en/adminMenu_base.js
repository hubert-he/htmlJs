var __GLOBAL__ = {
    pageRoot: ''
};
//2013-04-16 Wizard to Quick Setup
function generateNav() {
    var navs = {
        active: 0, 
        items: [ 
            {
                name: 'Status',
                sub: 0 
            },
#ifdef CONFIG_FAST_CONFIG
#ifdef CONFIG_VEND_NETCORE 
	    {
                name: 'Quick Start',
                sub: 1
            },
#else
			{
                name: 'Quick Setup',
                sub: 1
            },
#endif
#endif
            {
                name: 'Setup',
                sub: 2
            },
            {
                name: 'Advanced',
                sub: 3
            },
            {
                name: 'Service',
                sub: 4
            },
            {
                name: 'Firewall',
                sub: 5
            },
			{
                name: 'Maintenance',
                sub: 6
            }
        ]
    };
    return navs;
}
/**
 * 将nav的数据与模板拼接起来，然后渲染到页面
 */
function renderNav() {
    var nav = generateNav(); //获得导航数据
    var tpl = $('#nav-tmpl').html(); //获得nav模板数据
    var html = juicer(tpl, nav);
    $('#nav').html(html); //渲染到页面
}
/**
 * 生成第二级和第三级菜单的数据结构
 */
function generateSide() {
    var side = []; 
    var sub0, sub1, sub2, sub3, sub4, sub5, sub6;
    var pageRoot = __GLOBAL__.pageRoot;
    //第一个side
    sub0 = {
        key: 0, //第二级标识
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'Device_info',
                items: [
                    {
                        name: 'Device_info',
                        href: pageRoot + 'status.htm'
#if defined(CONFIG_ADSLUP)
                    },
                    {
                        name: 'ADSL',
                        href:  pageRoot + 'adslconfig.htm'
#endif
                    }
                ]
            },
            {
                collapsed: true,
                name: 'Statistics',
                items: [
                    {
                        name: 'Statistics',
                        href: pageRoot + 'stats.htm'
                    }
                ]
            }
        ]
    };
#ifdef CONFIG_FAST_CONFIG
	sub1 = {
        key: 1, //第二级标识
        active: '0-0',
        items: [
            {
                collapsed: false,
#ifdef CONFIG_VEND_NETCORE   
		name: 'Quick Start',
              items: [
                    {
                        name: 'Quick Start',
                        href: pageRoot + 'fc-page3-netcore.htm'
#else
//2013-04-16 Wizard to Quick Setup
                name: 'Quick Setup',
                items: [
                    {
                        name: 'Quick Setup',
                        href: pageRoot + 'fc-page3.htm'
#endif
                    }
                ]
            }
        ]
    };
#endif
    sub2 = {
        key: 2, 
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'WAN',
                items: [
			{
                        name: 'WAN',
                        href: pageRoot + 'wan.htm'
#ifdef CONFIG_USB_SERIAL_OPTION
			},
                    {
                        name: '3G',
                        href:  pageRoot + 'wan3gconf.htm'
                   
#endif
#if defined(CONFIG_ADSLUP)
			 },
	#ifdef CONFIG_AUTOPVC_SEARCH
					{
                        name: 'Auto PVC',
                        href:  pageRoot + 'autopvc.htm'
                    },
	#endif
                    {
                        name: 'ATM',
                        href:  pageRoot + 'wanatm.htm'
	#ifdef CONFIG_DSL_ANNEXB
					},
					//2013-12-23 org(adslset_annexb.htm)
                    {
                        name: 'ADSL',
                        href:  pageRoot + 'adslset.htm'
	#else
                    },
                    {
                        name: 'ADSL',
                        href:  pageRoot + 'adslset.htm'
	#endif
#endif
        		}
                ]
            },
            {
                collapsed: true,
                name: 'LAN',
                items: [
					{
                        name: 'LAN',
                        href: pageRoot + 'tcpiplan.htm'
                    },
					{
                        name: 'DHCP',
                        href: pageRoot + 'dhcpd.htm'
                    },
	#ifdef CONFIG_DHCP_MULTISERVER
                    {
                        name: 'DHCP Interface',
                        href: pageRoot + 'dhcpinterface.htm'
                    },
	#endif	
                    {
                        name: 'DHCP Static',
                        href: pageRoot + 'dhcpip.htm'
#ifdef INET6
                    },
                    {
                        name: 'LAN IPv6',
                        href: pageRoot + 'lan_ipv6.htm'
#endif
                    }
                ]
#ifdef CONFIG_WLAN
            },
            {
                collapsed: true,
                name: 'WLAN',
                items: [
                    {
                        name: 'Basic',
                        href: pageRoot + 'wlbasic.htm'
                    },
					{
                        name: 'Security',
                        href: pageRoot + 'wlwpa.htm'
	#ifdef CONFIG_MBSSID
		#ifndef CONFIG_INDONESIA_SW_FEATURES
                    },
                    {
                        name: 'MBSSID',
                        href: pageRoot + 'wlmbssid.htm'
              #else
		   #ifdef CONFIG_INDONESIA_SW_FEATURES_FOR_RFWELL
                    },
                    {
                        name: 'MBSSID',
                        href: pageRoot + 'wlmbssid.htm'
		   #endif
        	#endif
	#endif
	#ifdef CONFIG_USER_WLAN_ACL
                    },
                    {
                        name: 'Access Control List',
                        href: pageRoot + 'wlactrl.htm'
	#endif
                    },
                    {
                        name: 'Advanced',
                        href: pageRoot + 'wladvanced.htm'
	#ifdef CONFIG_WSC
		#ifdef CONFIG_VEND_TPLINK
			#ifdef CONFIG_PORTUGAL_SW_FEATRUES
                    },
                    {
                        name: 'WPS',
                        href: pageRoot + 'wlwps.htm'
			#else
					},
                    {
                        name: 'QSS',
                        href: pageRoot + 'wlqss.htm'
			#endif
		#else
					},
                    {
                        name: 'WPS',
                        href: pageRoot + 'wlwps.htm'
		#endif
	#endif
	#ifdef CONFIG_WDS
                    },
                    {
                        name: 'WDS',
                        href: pageRoot + 'wlwds.htm'
	#endif
                    }
                ]
#endif
        }
     ]		
  };

    sub3 = {
        key: 3, 
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'Route',
                items: [
                    {
                        name: 'Static Route',
                        href: pageRoot + 'routing.htm'
                    },
#ifdef INET6
                    {
                        name: 'IPv6 Static Route',
                        href:  pageRoot + 'routing_v6.htm'
                    },
#endif
                    {
                        name: 'RIP',
                        href:  pageRoot + 'rip.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'NAT',
                items: [
                    {
                        name: 'DMZ',
                        href: pageRoot + 'fw-dmz.htm'
                    },
                    {
                        name: 'Virtual Server',
                        href: pageRoot + 'virtualSrv.htm'
                    },
                    {
                        name: 'ALG',
                        href: pageRoot + 'fw-natpass.htm'
                    },
#ifndef CONFIG_VEND_TPLINK			
	#ifdef CONFIG_NAT_INSIDE_EXCLUDE_IP
                    {
                        name: 'NAT Exclude IP',
                        href: pageRoot + 'fw_excludeip.htm'
	#endif
#endif
#ifdef CONFIG_NAT_PORTRIGGER
                    },
                    {
                        name: 'Port Trigger',
                        href: pageRoot + 'nat_portrigger.htm'
#endif
#ifndef CONFIG_VEND_TPLINK
	#ifdef CONFIG_ALG_MULTIPORTS_SUPPORT
                    },
                    {
                        name: 'FTP ALG Port',
                        href: pageRoot + 'nat_ftpalg.htm'
	#endif
#endif
#ifdef CONFIG_IP_NAT_FOURTYPE
                    },
                    {
                        name: 'Nat IP Mapping',
#else
						name: 'NAT pool',
#endif
                        href: pageRoot + 'fw-natmapping.htm'

                    }
                ]
            },
            {
                collapsed: true,
                name: 'QoS',
                items: [
#ifndef IP_QOS_TELEFONICA
                    {
                        name: 'QoS',
                        href: pageRoot + 'ipqos.htm'
 #ifdef CONFIG_TRAFFIC_SHAPING
                    },
			{
                        name: 'Traffic Shaping',
                        href: pageRoot + 'ipqostc.htm'
#endif           
                    }
#else
					{
                        name: 'Priority Queue',
                        href: pageRoot + 'ipqosqueue.htm'
                    },
					{
                        name: 'IP QoS',
                        href: pageRoot + 'ipqos_t.htm'
#ifdef CONFIG_TRAFFIC_SHAPING
                    },
					{
                        name: 'Traffic Shaping',
                        href: pageRoot + 'ipqostc.htm'
#endif                  
		    }
#endif
                ]
#ifdef CONFIG_USER_CWMP_TR069
#if !defined(CONFIG_3BB_SW_FEATURES) &&!defined(CONFIG_OBSERVA_VIVO_1P) 
            },
            {
                collapsed: true,
                name: 'CWMP',
                items: [
                    {
                        name: 'CWMP',
                        href: pageRoot + 'tr069.htm'
                    }
                ]
#endif
#endif
#if  defined (CONFIG_RE8305) ||defined(CONFIG_RE8306)||defined(CONFIG_USB_OTG_DEV)||defined(CONFIG_WLAN)   || defined(CONFIG_RLE0412_4P_LAN) 
            },
            {
                collapsed: true,
                name: 'Port Mapping',
                items: [
                    {
                        name: 'Port Mapping',
                        href: pageRoot + 'portmap.htm'
                    }
                ]
#endif
#ifndef CONFIG_VEND_TPLINK
            },
            {
                collapsed: true,
                name: 'Others',
                items: [
                    {
                        name: 'Bridge Setting',
                        href: pageRoot + 'bridging.htm'
	#ifdef CONFIG_NETSNIPER_PREVENTION
                    },
					{
                        name: 'NetSniper Setting',
                        href: pageRoot + 'netsniper.htm'
	#endif
	#ifdef CONFIG_CLIENTS_LIMIT
                    },
                    {
                        name: 'Client Limit',
                        href: pageRoot + 'clientlimit.htm'
	#endif
	#ifdef CONFIG_IPV6_TUNNEL
					},
                    {
                        name: 'Tunnel',
                        href: pageRoot + 'tunnel.htm'
	#endif
                    },
                    {
                        name: 'Others',
                        href: pageRoot + 'others.htm'
                    }
                ]
#else
	#ifdef CONFIG_CLIENTS_LIMIT
			},
            {
                collapsed: true,
                name: 'Others',
                items: [
                    {
                        name: 'Client Limit',
                        href: pageRoot + 'clientlimit.htm'
	#endif
#endif
            }
        ]
        };
    sub4 = {
        key: 4, 
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'IGMP',
                items: [
                    {
                        name: 'IGMP Proxy',
                        href: pageRoot + 'igmproxy.htm'
#ifndef CONFIG_VEND_TPLINK
	#ifdef INET6
                    },
                    {
                        name: 'MLD',
                        href:  pageRoot + 'mld.htm'
	#endif			
#endif
                    }
                ]
            },
            {
                collapsed: true,
                name: 'UPnP',
                items: [
                    {
                        name: 'UPnP',
                        href: pageRoot + 'upnp.htm'
#ifdef CONFIG_MINIUPNP_DLNA_UPNPTASK
					},
					{
                        name: 'DLNA',
                        href: pageRoot + 'dlna.htm'
#endif
                    }
                ]
#ifdef CONFIG_SNMP
            }, 
            {
                collapsed: true,
                name: 'SNMP',
                items: [
                    {
                        name: 'SNMP',
                        href: pageRoot + 'snmp.htm'
                    }
                ]
#endif
#if !defined(CONFIG_DNS_BIND_PVC_SUPPORT)
#if !defined(CONFIG_RTL_819X)
            },
            {
                collapsed: true,
                name: 'DNS',
                items: [
                    {
                        name: 'DNS',
                        href: pageRoot + 'dns.htm'
	#ifdef INET6
                    },
                    {
                        name: 'IPv6 DNS',
                        href: pageRoot + 'dns_v6.htm'
	#endif
                    }
                ]
#endif
#endif
            },
            {
                collapsed: true,
                name: 'DDNS',
                items: [
                    {
                        name: 'DDNS',
                        href: pageRoot + 'ddns.htm'
                    }
                ]
#ifdef CONFIG_BFTPD_PAGE
		},
            {
                collapsed: true,
                name: 'FTP Server',
                items: [
                    {
                        name: 'FTP Server',
                        href: pageRoot + 'ftpd.htm'
                    }
                ]
#endif
#if defined(CONFIG_L2TP)||defined(CONFIG_PPTP_CLIENT)
			},
            {
                collapsed: true,
                name: 'VPN',
                items: [
	#ifdef CONFIG_L2TP
                    {
                        name: 'L2TP',
                        href: pageRoot + 'l2tp.htm'
                    }				
	#endif
	#if defined(CONFIG_L2TP)&&defined(CONFIG_PPTP_CLIENT)
	,
	#endif
	#ifdef CONFIG_PPTP_CLIENT
					{
                        name: 'PPTP',
                        href: pageRoot + 'pptp.htm'
                    }
	#endif
                ]
#endif
#ifdef CONFIG_APP_CUPS
			},
            {
                collapsed: true,
                name: 'USB Printer',
                items: [
                    {
                        name: 'USB Printer',
                        href: pageRoot + 'cups.htm'
                    }
                ]
#endif
            }
        ]
        };

    sub5 = {
        key: 5, 
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'MAC Filter',
                items: [
                    {
                        name: 'MAC Filter',
                        href: pageRoot + 'fw-macfilter.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'IP/Port Filter',
                items: [
#ifdef CONFIG_IPPORTFILTER_ADV
                    {
                        name: 'IP/Port Filter',
                        href: pageRoot + 'fw-ipportfilter_adv.htm'
#else
					{
                        name: 'IP/Port Filter',
                        href: pageRoot + 'fw-ipportfilter.htm'
#endif
#ifdef INET6
                    },
                    {
                        name: 'IPv6/Port Filter',
                        href: pageRoot + 'fw-ipportfilter_adv_v6.htm'
#endif
                    }
                ]
            },
            {
                collapsed: true,
                name: 'URL Filter',
                items: [
                    {
                        name: 'URL Filter',
                        href: pageRoot + 'url_nokeyword.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'ACL',
                items: [
                    {
                        name: 'ACL',
                        href: pageRoot + 'acl.htm'
#ifdef INET6
                    },
                    {
                        name: 'IPv6 ACL',
                        href: pageRoot + 'acl_v6.htm'
#endif
                    }
                ]
#ifdef  CONFIG_DOS
            },
            {
                collapsed: true,
                name: 'DoS',
                items: [
                    {
                        name: 'DoS',
                        href: pageRoot + 'dos.htm'
                    }
                ]
#endif
#ifdef CONFIG_IP_LAYER7_FILTER
			},
            {
                collapsed: true,
                name: 'Software Forbidden',
                items: [
                    {
                        name: 'Software Forbidden',
                        href: pageRoot + 'fw-layer7filter.htm'
                    }
                ]
#endif
            }
        ]
        };
    sub6 = {
        key: 6, 
        active: '0-0',
        items: [
            {
                collapsed: false,
                name: 'Update',
                items: [
#ifndef CONFIG_INDONESIA_SW_FEATURES
                    {
                        name: 'Firmware Update',
                        href: pageRoot + 'upload.htm'
                    },
#else
		   #ifdef CONFIG_INDONESIA_SW_FEATURES_FOR_RFWELL
                    {
                        name: 'Firmware Update',
                        href: pageRoot + 'upload.htm'
                    },
		   #endif
#endif
                    {
                        name: 'Backup/Restore',
                        href: pageRoot + 'saveconf.htm'
                    }
                ]
#ifdef CONFIG_ADD_USER 
            },
            {
                collapsed: true,
                name: 'Password',
                items: [
                    {
                        name: 'Password',
                        href: pageRoot + 'userconfig.htm'
                    }
                ]
#endif
            },
            {
                collapsed: true,
                name: 'Reboot',
                items: [
                    {
                        name: 'Reboot',
                        href: pageRoot + 'reboot.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'Time',
                items: [
                    {
                        name: 'Time',
                        href: pageRoot + 'time.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'Log',
                items: [
                    {
                        name: 'Log',
                        href: pageRoot + 'logging.htm'
                    }
                ]
            },
            {
                collapsed: true,
                name: 'Diagnostics',
                items: [
                    {
                        name: 'Ping',
                        href: pageRoot + 'ping.htm'
#ifdef INET6
                    },
                    {
                        name: 'Ping6',
                        href: pageRoot + 'ping_v6.htm'
#endif
#ifdef CONFIG_USER_TRACEROUTE
                    },
                    {
                        name: 'Traceroute',
                        href: pageRoot + 'traceroute.htm'
#endif
#ifdef CONFIG_USER_TRACEROUTE6
                    },
                    {
                        name: 'Traceroute6',
                        href: pageRoot + 'traceroute_v6.htm'
#endif
#if defined(CONFIG_ADSLUP)
                    },
                    {
                        name: 'OAM Loopback',
                        href: pageRoot + 'oamloopback.htm'
	#ifdef CONFIG_DSL_DIAG
                    },
                    {
                        name: 'ADSL Diagnostic',
                        href: pageRoot + 'adsl-diag.htm'
	#endif
#endif	
#ifdef CONFIG_DIAG_TEST
                    },
                    {
                        name: 'Diag-Test',
                        href: pageRoot + 'diag-test.htm'
#endif

                    }
                ]
            }
        ]
        }
    side.push(sub0);
#ifdef CONFIG_FAST_CONFIG
    side.push(sub1);
#endif
    side.push(sub2);
    side.push(sub3);
    side.push(sub4);
    side.push(sub5);
	side.push(sub6);
	
    return side;
}

function adaptNav(side, key) {
    key = (key - 0)
        || 0; //防止出现字符串类型
    var sideObj = {};
    for (var i = 0; i < side.length; i++) {
        if (side[i] && side[i].key === key) {
            sideObj.active = side[i].active;
            sideObj.items = side[i].items;
            for (var j = 0; j < sideObj.items.length; j++) {
                sideObj.items[j].index = j; //设置第二级的索引;
            }
            return sideObj;
        }
    }
}
/**
 * 将side的数据与模板拼接起来，然后渲染到页面
 * @param key
 */
function renderSide(key) {
    var side = adaptNav(generateSide(), key);
    var tpl = $('#side-tmpl').html();
    var html = juicer(tpl, side);
//    var html = $('#side-tmpl').render(side);
    $('#side').html(html);
}
/**
 * 高亮选中当前项
 */
function setActive(items, current) {
    $(items).removeClass('active');
    $(current).addClass('active');
}
/**
 * 折叠或展开side
 * @param item
 */
function setAccordion(item) {
    var $item = $(item);
    var className = 'collapsed';
    var $currentLi = $item.parents('li');

    var $allLi = $item.parents('#side').children('li');

    var $currentContent = $currentLi.children('ul');

    $allLi.addClass(className);
    $currentLi.removeClass(className);
   
}
