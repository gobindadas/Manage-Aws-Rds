python-rds:
 -> Create rds snapshot from rds db instance (create-snapshot.py)
 -> Restore snapshot with default or custom configuration (restore-snapshot.py)

 > Set environment for aws access and secret key
   Access and Secret key will be read from env variables.
   name should be: ACCESS_KEY and SECRET_KEY
   
 > Command to run script:
   For create snapshot:
    python create-snapshot.py -r region -i dbInstanceId
    Note:
      Both region and dbInstanceId mandatory.

   For Restore:
     python restore-snapshot.py -r regionName -i instanceId -s snapshotId -g subnetGroup -m multiAZ(true/false) -p port -t tags -L list
     Ex: python restore-snapshot.py -r us-west-1 -i test-rds -s test-rds-20161205-8321 -g default-vpc-bd67gh -m true -p 5432 -t '[{"Key": "devtag","Value": "dev"}]' -L list

    Command description:
        -r regionName -i instanceId -s snapshotId -g subnetGroup -m multiAZ(true/false) -p port -t tags -L list

    Mandatory : regionName,instanceId,snapshotId and subnetGroup
    Others are optional.
    multiAZ default is False
    port default is 5432

    Note: tags will be like: '[{"Key": "devtag","Value": "dev"}]'
           multiAZ : true/false
           -L is optional(if -L given then user will see all available snapshots)

Note: boto3 needs to be installed before running script.
