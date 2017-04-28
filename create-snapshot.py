#!/usr/bin/python

# Author: Gobinda Das
# Email: gobindamca2011@gmail.com
# Create aws rds db snapshot

import datetime
import boto3
import random
import os
import getopt, sys

snapshotFormat = '%(name)s-%(date)s'
today = datetime.date.today()

# Read access and secret keys from environment variable.
accessKey = os.environ.get("ACCESS_KEY")
secretKey = os.environ.get("SECRET_KEY")

def usage_exception():
  print 'Usage: '+sys.argv[0]+' -r <region> -i <instanceId>'

def usage():
  print 'Usage: '+sys.argv[0]+' -r <region> -i <instanceId>'
  sys.exit(0)

# Method to create snapshot from existing db instance
def create_snapshot(region, accessKey, secretKey, snapshotId, instanceId):
    try:
        # Create client to access aws api
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        # Create db snapshot
        client.create_db_snapshot(DBSnapshotIdentifier=snapshotId, DBInstanceIdentifier=instanceId)
        print ("Snapshot " + snapshotId + " created successfully.")
    except Exception, e:
        raise

def main(argv):
    region=""
    dbInstanceId=""
    try:
        try:
            optlist, args = getopt.getopt(argv, "r:i:help", ["r=","i=","help="])
            if not optlist:
                print 'No options supplied'
                usage()

            for o, a in optlist:
                if o == '-r':
                  region = a
                elif o == '-i':
                  dbInstanceId = a
                elif o == '-h':
                    usage()
                elif o == "--help":
                    usage()
            if region == "":
                usage()
            if dbInstanceId == "":
                usage()

        except Exception, e1:
            usage_exception()
            raise
        print("The supplied arguments are:  \n region: " + region  + " dbinstanceid: " + dbInstanceId )


        # Create snapshotId with instanceId,year,month and date
        snapshot_id = snapshotFormat % {'name': dbInstanceId, 'date': today.strftime('%Y%m%d')}

        # Attach some random number to snapshotId
        snapshot_id = snapshot_id + "-" + str(random.randint(1000, 10000))
        create_snapshot(region, accessKey, secretKey, snapshotId=snapshot_id, instanceId=dbInstanceId)
    except Exception, e:
        raise

    #main()
if __name__ == "__main__":
    main(sys.argv[1:])
