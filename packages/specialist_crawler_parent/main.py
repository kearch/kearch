from kearch_common.connection import KearchRequester


CRAWLER_CHILD_IP = '192.168.11.10'
CRAWLER_CHILD_PORT = 10080

DATABASE_IP = '192.168.11.11'
DATABASE_PORT = 10080

REQUESTER_NAME = 'specialist_crawler_parent'

if __name__ == '__main__':
    crawl_requester = KearchRequester(CRAWLER_CHILD_IP, CRAWLER_CHILD_PORT, REQUESTER_NAME)
    database_requester = KearchRequester(DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)
