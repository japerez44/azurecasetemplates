# Azurecasetemplates
This repository holds three folders: "v1", "v2" and "v3" corresponding to a possible solution for three Microsoft Azure "challenges", relating Infraestructure as a code. Each scenario is an incremental extension from the other. You cannot go to v3 solution if you don't have pass by v2 and so.

# V1 Scenario:
Requirements:
    • Deploy a VM running an Ubuntu server 22.04 lts gen 2
    • This VM must be accessible through Bastion with username & password
    • The VM must not have direct access to the Internet, instead its traffic must pass through an Azure Firewall (created aswell):
        •	In fact, all the traffic in the subnet on which the VM is deployed must be routed to the Firewall.
        •	The Firewall must allow all outgoing traffic from the subnet to the Internet and deny all other traffic.
Other Considerations:
    • Tighten the security in the subnet for the VNet by denying all incoming traffic from the Internet but allowing all outgoing traffic to the latter
    • Location for all resources is configurable (Spain Central in these examples).
    • Avoid "hardcoded" values for parameters to define resources. Names, passwords, OS version, VM size, locations for all resources, networks and all critical parameters have to be configurable (a Parameters File has been used for this purpose).
    • Try to make VNet address space configurable too
    • Notice that, after a reboot, the VM must keep its access to the Internet
Deliverables:
    - Full and complete ARM template for all resources ("azure_deployment_template.json" file in v1 folder)
    - Paremeters file ("azure_parameters.json")

# V2 Scenario (incremental from V1):
Requirements
    • Install an Apache server and activate HTTPS using the default configurations on the VM
    • Allow HTTP & HTTPS connections to the Apache server from the Internet through the Azure firewall.
Deliverables
    - ARM template & Parameters file ("azure_deployment_templatev2.json" & "azure_parametersv2.json")
    - Cloud Init script to install needed files during VM redeployment ("cloud_init_scriptv2.yaml")

# V3 Scenario (extend from previous deployment):
Requirements
    • If there is not a data disk on the VM, create a new one
    • Attach the data disk to the VM and use it as the DocumentRoot for both HTTP & HTTPS configuration
    • For Apache HTTP Server, enforce TLS 1.2 as Minimum Protocol and configure Cipher Suites according to Mozilla Intermediate Cipher Suite Configuration (https://ssl-config.mozilla.org/#server=apache&version=2.4.60&config=intermediate&openssl=3.4.0&hsts=false&ocsp=false&guideline=5.7).
    • Retrieve HTTPS certificate and private key from Azure Key Vault using Microsoft Entra ID Service Principal in a self-contained Python script, without using any external components like Azure SDK, Azure CLI, etc. The script should only use built-in Python modules.
Deliverables
    - ARM template & Parameters file ("azure_deployment_templatev3.json" & "azure_parametersv3.json")
    - Cloud Init script ("cloud_init_scriptv3.yaml")
    - A Python program for extracting certificate PFX through an Azure Key Vault using MS Entra ID ("retrivehttpscert.py" in v3 folder)
    - A draft of a specification document, including functional and non-functional specifications, encompassing the final product. This ReadMe.MD file out of v1, v2 or v3 folders.


# INSTRUCTIONS:
For running scenario V1, execute the following steps:
  - Login to Azure Portal
  - Open a Bash Cloud Shell (CLI) and upload ARM template and parameters file (inside v1 folder on this GIT) to $HOME filesystem and run sequentially:
    
          * az group create --name GrpRes1 --location spaincentral
    
          * az deployment group create \
              --resource-group GrpRes1 \
              --template-file azure_deployment_template.json \
              --parameters @azure_parameters.json
    
    @"GrpRes1" can be whatever, and "spaincentral" should be any other location, but then, you´ll have to set the same value in the Parameters file
  - if it is succeessfull, it will have created: a Bastion (the only way to access to the VM), a Firewall, 2x public IPs (for Bastion and Firewall services), an Ubuntu VM, one disk and one nic for the VM, a routing table, a security group for the subnet and a virtual network for all these elements.
Parameters file is totally configurable and you can use other values as you need them. However, you'll have to set then same values on v2&v3 parameters files...


For running scenario V2, execute the following steps:
  - Open a Bash Cloud Shell (CLI) and upload ARM template and parameters file for v2 challenge
  - As we have to redeploy a VM with some modifications from the previous one, we remove first from our resources group with the following command:
    
          * az vm delete \
              --resource-group GrpRes1 \
              --name myUbuntuVM \
              --yes
    
    @use the resource group & VM names you set on the previous scenario
  - and after that:
    
          * az deployment group create \
              --resource-group GrpRes1 \
              --template-file azure_deployment_templatev2.json \
              --parameters @azure_parametersv2.json
    
  - if everything is fine, you could access throuh internet to a simmple HTTP(S) web page on the VM, across the deployed Azure Firewall.


Same for scenario V3:
  - Open a Bash Cloud Shell (CLI) and upload ARM template and parameters file for v3 challenge
  - Remove VM first from our resources group with the following command:
    
          * az vm delete \
              --resource-group GrpRes1 \
              --name myUbuntuVM \
              --yes
    
  - and after that:
    
          * az deployment group create \
              --resource-group GrpRes1 \
              --template-file azure_deployment_templatev3.json \
              --parameters @azure_parametersv3.json
  
  - we will end up with a VM accessible from the internet (only by HTTP(S) through an firewall infraestructure deployed on Microsoft Azure.

Additionally, using the Python script "retrivehttpscert.py" on v3 folder, you could extract the certificate (PFX: public certificate plus private key) setting proper values to some variables inside the script:

    && REPLACE THESE ENTRY PARAMETERS with your actual values
    client_id = "your-cliend-id"
    client_secret = "<secret>"
    tenant_id = "your-tenant-id"
    keyvault_name = "keyvault-name"
    certificate_name = "certificate-name"


That's all. Thank you all.
