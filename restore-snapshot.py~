# Author: Gobinda Das
# Email: gobindamca2011@gmail.com
# Restore aws rds db snapshot

import boto3
import time
import os
import getopt, sys
import random
import simplejson as json

# Read access and secret keys from environment variable.
accessKey = os.environ.get("ACCESS_KEY")
secretKey = os.environ.get("SECRET_KEY")


def track_instance(region, accessKey, secretKey, instanceId, newInstanceId):
    print "Tracking instance for completion.."
    # Track till snapshot restore completed then delete old instance
    flag = True
    status = get_instance_details(region, accessKey, secretKey, instanceId)
    while flag:
        print "Current status: ", status
        if status == "available":
            check_delete_instance(region, accessKey, secretKey, newInstanceId)
            flag = False
        else:
            status = get_instance_details(region, accessKey, secretKey, instanceId)


def get_instance_details(region, accessKey, secretKey, instanceId):
    try:
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        response = client.describe_db_instances(DBInstanceIdentifier=instanceId)
        return response["DBInstances"][0]["DBInstanceStatus"]
    except Exception, e:
        return
    return


def modify_instance(region, accessKey, secretKey, instanceId, newInstanceId):
    try:
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        response = client.describe_db_instances(DBInstanceIdentifier=instanceId)
        if response is not None:
            print "Instance present"
            response1 = client.modify_db_instance(DBInstanceIdentifier=instanceId,
                                                  NewDBInstanceIdentifier=newInstanceId,
                                                  ApplyImmediately=True)
            print "Please wait for a sec,Instance name is changing..."
            time.sleep(60)
            return
        else:
            return
    except Exception, e:
        return
    return


# Delete Existing instance if available
def check_delete_instance(region, accessKey, secretKey, instanceId):
    try:
        # Create client to access aws api
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        response = client.describe_db_instances(DBInstanceIdentifier=instanceId)
        if response is not None:
            print "Instance present"
            response = client.delete_db_instance(DBInstanceIdentifier=instanceId, SkipFinalSnapshot=True)
            print "Wait till instance deletion complete....."
            # time.sleep(450)
            return
        else:
            print "No Instance available"
            return
    except Exception, e:
        return
    return


def restore_snapshot(region, accessKey, secretKey, instanceId, newInstanceId, snapshotId, subnetGroup, multiAZ, port,
                     tags):
    try:
        # Create client to access aws api
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        # Restore snapshot with tags
        if tags:
            response = client.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=instanceId,
                                                                   DBSnapshotIdentifier=snapshotId,
                                                                   DBSubnetGroupName=subnetGroup,
                                                                   MultiAZ=multiAZ, Port=port,
                                                                   Tags=tags)
            print "Please wait till restore completed with tags...."
            time.sleep(500)
        # Restore snapshot without tags
        else:
            response = client.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=instanceId,
                                                                   DBSnapshotIdentifier=snapshotId,
                                                                   DBSubnetGroupName=subnetGroup,
                                                                   MultiAZ=multiAZ, Port=port)
            print "Please wait till restore completed without tags...."
            time.sleep(500)
    except Exception, e1:
        print("Exception.......")
        # Revert back existing instance if restore failed
        modify_instance(region, accessKey, secretKey, newInstanceId, instanceId)
        #sys.exit(0)
        raise
    return


def list_snapshots(region, accessKey, secretKey):
    try:
        client = boto3.client('rds', region_name=region, aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
        response = client.describe_db_snapshots()
        print "Available Snapshots: "
        for j in response["DBSnapshots"]:
            print j["DBSnapshotIdentifier"]
    except Exception, e:
        raise
    return

def validate(region,instanceId,snapshotId,subnetGroup):
    if region == "":
        usage()
    if instanceId == "":
        usage()
    if snapshotId == "":
        usage()
    if subnetGroup == "":
        usage()

def usage_exception():
  print 'Usage: '+sys.argv[0]+' -r <region> -i <instanceId> -s <snapshotId> -g <subnetGroup> -m [multiAZ] -p [port] -t [tags] -L [list]'

def usage():
  print 'Usage: '+sys.argv[0]+' -r <region> -i <instanceId> -s <snapshotId> -g <subnetGroup> -m [multiAZ] -p [port] -t [tags] -L [list]'
  sys.exit(0)

def main(argv):
    region=""
    snapshotId=""
    instanceId=""
    subnetGroup=""
    port = ""
    multiAZ= False
    try:
        try:
            optlist, args = getopt.getopt(argv, 'r:s:i:m:g:p:t:L:help')
            listOption=""
            tags=""
            if not optlist:
                print 'No options supplied'
                usage()
            for o, a in optlist:
                if o == "-r":
                    region = a
                    print "region:" , region
                elif o == "-s":
                    snapshotId = a
                    print "snapshotid:" , snapshotId
                elif o == "-i":
                    instanceId = a
                    print "instanceId: " , instanceId
                elif o == "-m":
                    multiAZ = bool(a)
                    print "multiAZ: ", multiAZ
                elif o == "-g":
                    subnetGroup = a
                    print "subnetGroup: ", subnetGroup
                elif o == "-p":
                    port = int(a)
                    print "port: ", port
                elif o == "-t":
                    tags = json.loads(a)
                    print "tags: ", tags
                elif o == "-L":
                    listOption = o
                    print (listOption)
                elif o == '-h':
                    usage()
                elif o == "--help":
                    usage()
        except Exception, e1:
            usage_exception()
            raise
        # Validate Inputs
        validate(region, instanceId, snapshotId, subnetGroup)

        if listOption == "-L":
            # List out all available snapshots
            list_snapshots(region, accessKey, secretKey)

        if port == "":
            port = 5432

        newInstanceId = instanceId + "-" + str(random.randint(1000, 10000))
        modify_instance(region, accessKey, secretKey, instanceId, newInstanceId)  # Restore snapshot with tags
        if tags:
            print "tags: ", tags
            restore_snapshot(region, accessKey, secretKey, instanceId, newInstanceId, snapshotId, subnetGroup, multiAZ,
                         port, tags)
            print "Restore completed..."
            track_instance(region, accessKey, secretKey, instanceId, newInstanceId)

    # Restore snapshot without tags
        else:
            print "no tags passed"
            restore_snapshot(region, accessKey, secretKey, instanceId, newInstanceId, snapshotId, subnetGroup, multiAZ,
                         port, "")
            print "Restore completed."
            track_instance(region, accessKey, secretKey, instanceId, newInstanceId)
    except Exception, e:
        raise

main(sys.argv[1:])
