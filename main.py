from calendars import Nosotros, IM, WC, Velez, Holidays
from pprint import pprint

def main():
    a = Nosotros()
    pprint(a.events.all)

if __name__ == '__main__':
    main()
