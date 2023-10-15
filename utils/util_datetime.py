from datetime import datetime

def now(flag=0):
    return datetime.utcnow()

if __name__ == '__main__':
    print (now())