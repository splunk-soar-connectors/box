[comment]: # "Auto-generated SOAR connector documentation"
# Box

Publisher: Splunk Community  
Connector Version: 1\.0\.2  
Product Vendor: Box  
Product Name: Box  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.0\.0  

Perform various actions in a box environment

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2021 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
Follow the steps outlined in this link and use the supplemental notes below:
<https://developer.box.com/docs/setting-up-a-jwt-app>  
  
Step 1 Notes:  
\*Choose "Custom App" when setting up  
\*Make sure "Generate User Access Tokens" is switched on in "Advanced Features"  
  
Step 2 Notes: Use the following instructions to generate public/private keypair:  
  
1. Click on your JWT app from the developer console.  
2. Click on the Configuration option from the left nav.  
3. Scroll down to the Add and Manage Public Keys section.  
4. Click on the button to Generate a Public/Private Keypair.  
  
  
Be sure to download the pair as you will not be able to retrieve the private key later on. Also,
keep in mind this is an encrypted private key, so it will need to be decrypted.  
  
Once you have completed the app setup, you will need to configure the asset in Phantom.  
  
\* The private key needs to be the value in between '-----BEGIN PRIVATE KEY-----' AND '-----END
PRIVATE KEY-----'

The app uses HTTP/ HTTPS protocol for communicating with the Box server. Below are the default ports
used by Splunk SOAR.

|         Service Name | Transport Protocol | Port |
|----------------------|--------------------|------|
|         http         | tcp                | 80   |
|         https        | tcp                | 443  |


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Box asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**client\_id** |  required  | string | Client ID
**client\_secret** |  required  | password | Client secret
**public\_key** |  required  | string | Public key
**private\_key** |  required  | password | Private key \(decrypted\)
**box\_user\_id** |  required  | string | User ID found on app general screen
**box\_key\_id** |  required  | string | Key ID of the box key pair being used \(located on configuration page\)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[upload file](#action-upload-file) - Upload file to a box folder  
[create folder](#action-create-folder) - Create a folder in box  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'upload file'
Upload file to a box folder

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file\_name** |  required  | Name of file to be created | string | 
**folder\_id** |  required  | Box folder ID to create file in\. Enter "0" to create in root | string | 
**vault\_id** |  required  | Phantom vault ID of file to be created in box | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.file\_name | string | 
action\_result\.parameter\.folder\_id | string | 
action\_result\.parameter\.vault\_id | string | 
action\_result\.status | string | 
action\_result\.summary\.file\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.summary\.sha1 | string |   

## action: 'create folder'
Create a folder in box

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**folder\_name** |  required  | Name of folder to be created | string | 
**parent\_id** |  required  | Box folder ID to create folder in\. Enter "0" to create in root | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.parent\_id | string | 
action\_result\.parameter\.folder\_name | string | 
action\_result\.status | string | 
action\_result\.summary\.folder\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.data\.\*\.item\_collection\.total\_count | numeric | 
action\_result\.data\.\*\.item\_collection\.limit | numeric | 
action\_result\.data\.\*\.item\_collection\.offset | numeric | 
action\_result\.data\.\*\.size | numeric | 
action\_result\.data\.\*\.purged\_at | string | 
action\_result\.data\.\*\.folder\_upload\_email | string | 
action\_result\.data\.\*\.shared\_link | string | 
action\_result\.data\.\*\.path\_collection\.total\_count | numeric | 
action\_result\.data\.\*\.path\_collection\.entries\.\*\.sequence\_id | string | 
action\_result\.data\.\*\.path\_collection\.entries\.\*\.etag | string | 
action\_result\.data\.\*\.trashed\_at | string | 
action\_result\.data\.\*\.parent\.sequence\_id | string | 
action\_result\.data\.\*\.parent\.etag | string | 