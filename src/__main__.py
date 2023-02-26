import datetime
import typing

import requests
import ics

def cvtStr2Datetime(datestring: str, pattern: str = '%Y-%m-%d') -> datetime.datetime:
    return datetime.datetime.strptime(datestring, pattern)

def cvtInt2Datetime(ms: int) -> datetime.datetime:
    head = datetime.datetime(1970, 1, 1)
    offset = datetime.timedelta(0, 0, 0, ms)
    return head + offset

def loadCalendarJSON() -> typing.Dict[str, typing.Any]:
    response = requests.post(
        url="https://www.smu.ac.kr/app/common/selectDataList.do",
        data={
            'sqlId': 'jw.Article.selectCalendarArticle',
            'modelNm': 'list',
            'jsonStr': '{"year":"2023","bachelorBoardNoList":["85"]}',
        }
    )
    return response.json()

def loadCalendarICS(calendarJSON) -> ics.icalendar.Calendar:
    if not calendarJSON["success"]:
        return
    calendar =  ics.icalendar.Calendar(creator="상명대학교 (+hepheir@gmail.com)")
    for eventJSON in calendarJSON["list"]:
        event = ics.event.Event(
            name = eventJSON["articleTitle"],
            begin = cvtStr2Datetime(eventJSON["etcChar6"]),
            end = cvtStr2Datetime(eventJSON["etcChar7"]),
            uid = str(eventJSON["articleNo"]),
            # description: str = None,
            created = cvtInt2Datetime(eventJSON["createDt"]),
            last_modified = cvtInt2Datetime(eventJSON["updateDt"]),
            # location: str = None,
            url = "https://www.smu.ac.kr/ko/life/academicCalendar.do",
            # transparent: bool = None,
            # alarms: Iterable[BaseAlarm] = None,
            # attendees: Iterable[Attendee] = None,
            # categories: Iterable[str] = None,
            # status: str = None,
            # organizer: Organizer = None,
            # geo=None,
            # classification: str = None,
        )
        calendar.events.add(event)
    return calendar

def main():
    calendar = loadCalendarICS(loadCalendarJSON())
    with open("docs/calendar.ics", 'w') as icsFile:
        icsFile.writelines(calendar.serialize_iter())

main()