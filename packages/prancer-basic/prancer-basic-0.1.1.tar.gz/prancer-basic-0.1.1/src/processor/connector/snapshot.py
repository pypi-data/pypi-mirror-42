"""
   Common file for running snapshot functions.
"""
import json
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    get_container_snapshot_json_files, SNAPSHOT, JSONTEST,\
    collectiontypes, get_json_files, TEST
from processor.helper.config.config_utils import config_value, framework_dir
from processor.database.database import DATABASE, DBNAME, get_documents, sort_field
from processor.connector.snapshot_azure import populate_azure_snapshot
from processor.connector.snapshot_custom import populate_custom_snapshot
from processor.connector.snapshot_aws import populate_aws_snapshot


logger = getlogger()
snapshot_fns = {
    'azure': populate_azure_snapshot,
    'git': populate_custom_snapshot,
    'aws': populate_aws_snapshot
}


def populate_snapshot(snapshot):
    snapshot_type = get_field_value(snapshot, 'type')
    if snapshot_type and snapshot_type in snapshot_fns:
        if 'nodes' not in snapshot or not snapshot['nodes']:
            logger.info("No nodes in snapshot to be backed up!...")
            return False
        return snapshot_fns[snapshot_type](snapshot)
    return False


def populate_snapshots_from_json(snapshot_json_data):
    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.info("Json Snapshot does not contain snapshots, next!...")
        return False
    for snapshot in snapshots:
        populate_snapshot(snapshot)
    return True


def populate_snapshots_from_file(snapshot_file):
    """Load the file as json and populate from json file."""
    snapshot_json_data = json_from_file(snapshot_file)
    if not snapshot_json_data:
        logger.info("Snapshot file %s looks to be empty, next!...", snapshot_file)
        return False
    logger.debug(json.dumps(snapshot_json_data, indent=2))
    return populate_snapshots_from_json(snapshot_json_data)


def populate_container_snapshots(container, dbsystem=True):
    if dbsystem:
        return populate_container_snapshots_database(container)
    else:
        return populate_container_snapshots_filesystem(container)


def populate_container_snapshots_filesystem(container):
    """ Get the snapshot files in the container"""
    snapshot_dir, snapshot_files = get_container_snapshot_json_files(container)
    if not snapshot_files:
        logger.info("No Snapshot files in %s, exiting!...", snapshot_dir)
        return False
    logger.info('\n'.join(snapshot_files))
    snapshots = container_snapshots_filesystem(container)
    populated = []
    for snapshot_file in snapshot_files:
        parts = snapshot_file.rsplit('/', 1)
        if parts[-1] in snapshots and parts[-1] not in populated:
            populate_snapshots_from_file(snapshot_file)
            populated.append(parts[-1])
    return True


def populate_container_snapshots_database(container):
    """ Get the snapshot files from the database"""
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    if docs and len(docs):
        logger.info('Number of Snapshot Documents: %s', len(docs))
        snapshots = container_snapshots_database(container)
        populated = []
        for doc in docs:
            if doc['json']:
                snapshot = doc['name']
                if snapshot in snapshots and snapshot not in populated:
                    populate_snapshots_from_json(doc['json'])
                    populated.append(snapshot)
    return True


def container_snapshots_filesystem(container):
    """Get snapshot list used in test files from the filesystem."""
    snapshots = []
    logger.info("Starting to get list of snapshots")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        test_json_data = json_from_file(test_file)
        if test_json_data:
            snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
            if snapshot:
                snapshots.append(snapshot)
    return list(set(snapshots))


def container_snapshots_database(container):
    """Get snapshot list used in test files from the filesystem."""
    snapshots = []
    logger.info("Starting to get list of snapshots from database")
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[TEST])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    logger.info('Number of test Documents: %s', len(docs))
    if docs and len(docs):
        for doc in docs:
            if doc['json']:
                snapshot = doc['json']['snapshot'] if 'snapshot' in doc['json'] else ''
                if snapshot:
                    snapshots.append(snapshot)
    return list(set(snapshots))