'''This module is designed to automatically remove access rights to Google drive files'''
import logging
from os import environ
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
EMAIL = environ.get('EMAIL_ADDRESS')

def get_logger():
    '''Logging function'''
    date_format = '%Y-%m-%d %H:%M:%S %z'
    logger = logging.getLogger('unsharing-tool')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',
                                  datefmt=date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

LOGGER = get_logger()

def init_api():
    '''Initial Google Drive API function'''
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_files(service):
    '''Function for obtaining list of files in google drive'''
    return service.files().list(fields='files(id, name, permissions(id, emailAddress))').execute()

def remove_permission(service, file_id, file_name, permission_id):
    '''Function for removing permission rule from file '''
    service.permissions().delete(fileId=file_id,
                                 permissionId=permission_id).execute()
    LOGGER.info("%s. Permission for %s removed", file_name, EMAIL)

def main():
    '''Main function'''
    creds = init_api()

    service = build('drive', 'v3', http=creds.authorize(Http()))

    files = get_files(service)
    count = 0

    for item in files['files']:
        if 'permissions' in item:
            for permission in item['permissions']:
                if 'emailAddress' in permission:
                    if permission['emailAddress'].lower() == EMAIL.lower():
                        remove_permission(service,
                                          item['id'],
                                          item['name'],
                                          permission['id'])
                        count += 1
        #else:
            #LOGGER.info("%s. Requested user can't share this item" %
            #            item['name'])
    LOGGER.info('Permissions removed for %d files.', count)

if __name__ == '__main__':
    main()
