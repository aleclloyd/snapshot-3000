# snapshot-3000
python demo project

Demo project to manage AWS ec2 instance snapshots

##about
this prokect is a demo and uses boto3 to manage the AWS ec2 instance snapshots

##configuring
shotty uses the configuration file created by the AWS cli e.g.
`aws configure --profgile shotty`

##running

`pipenv run python shjotty/shotty.py` <command> <subcommandf> <--project=PROJECT>

*command* is instances, volumes, or snapshots
*sub command* depends on command
*project* is optional