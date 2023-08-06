# linkinvclient
python and CLI client for linkinventory micoservie 




Installation
================================

    git clone https://github.com/microservice-tsp-billing/llinkInventory.git
    cd llinkInventory
    virtualenv -p python3 venv
	source venv/bin/activate
	pip install -r requirement.txt


pip install coming soon
----------------------------

config
===============================================================
Follow readme for configuring the tokenleaderclient first - https://github.com/microservice-tsp-billing/linkinvclient
apart from the tokenleaderclient configuration  the following sections should be present in the /etc/tokenleader/client_configs.yml


	llinkInventory:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
  
  
hence the complete configuraion will look as:  


    user_auth_info_from: file # OSENV or file
	user_auth_info_file_location: /home/bhujay/tlclient/user_settings.ini
	fernet_key_file: /home/bhujay/tlclient/prod_farnetkeys	
	tl_public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYV9y94je6Z9N0iarh0xNrE3IFGrdktV2TLfI5h60hfd9yO7L9BZtd94/r2L6VGFSwT/dhBR//CwkIuue3RW23nbm2OIYsmsijBSHtm1/2tw/0g0UbbneM9vFt9ciCjdq3W4VY8I6iQ7s7v98qrtRxhqLc/rH2MmfERhQaMQPaSnMaB59R46xCtCnsJ+OoZs5XhGOJXJz8YKuCw4gUs4soRMb7+k7F4wADseoYuwtVLoEmSC+ikbmPZNWOY18HxNrSVJOvMH2sCoewY6/GgS/5s1zlWBwV/F0UvmKoCTf0KcNHcdzXbeDU9/PkGU/uItRYVfXIWYJVQZBveu7BYJDR bhujay@DESKTOP-DTA1VEB
	tl_user: user1
	tl_url: http://localhost:5001
	ssl_verify: False	
	llinkInventory:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
 


PYTHON client
===================================

	from tokenleaderclient.configs.config_handler import Configs
	from  tokenleaderclient.client.client import Client
	from linkinvclient.client import LIClient
	auth_config = Configs()
	tlclient = Client(auth_config)
	c = LIClient(tlclient)
	c.list_links()


from tokenleaderclient.configs.config_handler import Configs
from  tokenleaderclient.client.client import Client
from linkinvclient.client import LIClient
auth_config = Configs()
tlclient = Client(auth_config)
c = LIClient(tlclient)
c.list_links()
c.list_link_by_slno(1)

CLI coming soon
=====================
     
     linkinv.sh  list -n all
     linkinv.sh  list -n 1
     
 or when  pip installation from package is not done and you are running from the source 
     
    ./linkinv.sh  list -n all
    ./linkinv.sh  list -n 1
    
    
