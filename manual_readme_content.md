[comment]: # " File: README.md"
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
