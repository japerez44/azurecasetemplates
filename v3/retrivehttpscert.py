import http.client
import json
import base64
import ssl

# This function gets access token (returned value) or prints founded error from Microsoft Entra ID.
# Entry parameters:
#   - myclientid: Client ID from Microsoft Entra ID
#   - myclientsecret: Client secret
#   - mytenantid: Tenant ID from Microsoft Azure Entra ID

def getTokenEntra(myclientid, myclientsecret, mytenantid):
    myconn = http.client.HTTPSConnection("login.microsoftonline.com", context=GLOBALCONTEXT)
    mypayload = f"grant_type=client_credentials&client_id={myclientid}&client_secret={myclientsecret}&resource=https%3A%2F%2Fvault.azure.net"
    myheaders = {'Content-Type': 'application/x-www-form-urlencoded'}
    myconn.request("POST", f"/{mytenantid}/oauth2/token", mypayload, headers=myheaders)
    myres = myconn.getresponse()
    mydata = myres.read()
    mytokenresponse = json.loads(mydata.decode("utf-8"))
    try:
        myaccesstoken = mytokenresponse["access_token"]
        return myaccesstoken
    except:
        print (mytokenresponse)



# This function tries to print PFX Certificate from a Key Vault store. Otherwise, prints founded error.
# Entry parameters:
#   - myaccesstoken: Valid access token to Microsoft Entra ID
#   - mykeyvaultname: Key Vault name used as store
#   - mycertificatename: Certificate name within Key Vault store
#   - myapiversion: (optional) API version for extracting certificate. Default value: 7.3

def retrieveKeyVaultPFXCertificate(myaccesstoken, mykeyvaultname, mycertificatename, myapiversion = "7.3"):
    if not myaccesstoken:
        print ("ERROR: There is no valid access token")
        return
    myconn = http.client.HTTPSConnection(f"{mykeyvaultname}.vault.azure.net", context=GLOBALCONTEXT)
    myheaders = {
        'Authorization': f'Bearer {myaccesstoken}',
        'Content-Type': 'application/json'
    }
    # Retrieve certificate from Azure Key Vault
    myconn.request("GET", f"/certificates/{mycertificatename}?api-version={myapiversion}", headers=myheaders)
    myres = myconn.getresponse()
    mydata = myres.read()
    mycertmetadata = json.loads(mydata.decode("utf-8"))
    # Get the certificate's secret
    try:
        mysecretid = mycertmetadata["sid"].split("/")[-1]
        myconn.request("GET", f"/secrets/{mysecretid}?api-version={myapiversion}", headers=myheaders)
        myres = myconn.getresponse()
        mydata = myres.read()
        mysecretresponse = json.loads(mydata.decode("utf-8"))
        try:
            mypfxbase64 = mysecretresponse["value"]
            # Decodes and finally prints PFX certificate content
            print (base64.b64decode(mypfxbase64))
        except:
            print (mysecretresponse)
    except:
        print (mycertmetadata)
    



# REPLACE THESE ENTRY PARAMETERS with your actual values
client_id = "your-cliend-id"
client_secret = "<secret>"
tenant_id = "your-tenant-id"
keyvault_name = "keyvault-name"
certificate_name = "certificate-name"

# I decide to disable globally SSL checks just for convenience. However, it is not a best practice.
GLOBALCONTEXT = ssl.create_default_context()
GLOBALCONTEXT.check_hostname = False # this line can be removed for enabling SSL checks
GLOBALCONTEXT.verify_mode = ssl.CERT_NONE # this line can be removed for enabling SSL checks

# Step 1: Get access token from Microsoft Entra ID
access_token = getTokenEntra(client_id, client_secret, tenant_id)
# Step 2: If we have a valid access token, retrieve decoded certificate from Azure Key Vault
if access_token:
    retrieveKeyVaultPFXCertificate(access_token, keyvault_name, certificate_name)