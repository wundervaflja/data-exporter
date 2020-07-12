Azimu Git CLI

Provides command line integration point with Azimu.

Supported git services:

1. Bitbucket


How to run:
1. git clone https://gitlab.com/yudovenko/azimu-data-exporter.git
2. cd path azimu-data-exporter
3. pip install -r requirements.txt
3. update config file, vim config.yml
    * azimu_api.host, azimu_api.port, azimu_api.auth_token will be provided via email
    * fill bitbucket section by guide from Azimu 
4. python src/cli.py - run python script to send git metadata to Azimu
