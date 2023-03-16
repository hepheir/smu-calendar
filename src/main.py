import datetime
import typing

import requests
import ics

################################################################################

ICS_AUTHOR = "상명대학교 (+hepheir@gmail.com)"
ICS_FILE_OUTPUT_PATH = "docs/calendar.ics"

################################################################################

def cvtStr2Datetime(datestring: str, pattern: str = '%Y-%m-%d') -> datetime.datetime:
    return datetime.datetime.strptime(datestring, pattern)

def cvtInt2Datetime(ms: int) -> datetime.datetime:
    return datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=ms)

def loadCalendarJSON(year: int) -> typing.Dict[str, typing.Any]:
    response = requests.post(
        url="https://www.smu.ac.kr/app/common/selectDataList.do",
        data={
            'sqlId': 'jw.Article.selectCalendarArticle',
            'modelNm': 'list',
            'jsonStr': f'{{"year":"{year}","bachelorBoardNoList":["85"]}}',
        }
    )
    return response.json()

def parseCalendarJSON(calendarJSON: typing.Dict[str, typing.Any]) -> typing.Iterable[ics.event.Event]:
    if not calendarJSON["success"]:
        return
    for eventJSON in calendarJSON["list"]:
        try:
            event = ics.event.Event(
                name = eventJSON["articleTitle"],
                begin = cvtStr2Datetime(eventJSON["etcChar6"]),
                end = cvtStr2Datetime(eventJSON["etcChar7"]),
                uid = str(eventJSON["articleNo"]),
                created = cvtInt2Datetime(eventJSON["createDt"]),
                last_modified = cvtInt2Datetime(eventJSON["updateDt"]),
                url = "https://www.smu.ac.kr/ko/life/academicCalendar.do", # smu.ac.kr 학사일정 페이지 URL
            )
            event.make_all_day()
            yield event
        except:
            print("failed to add an event")
    return

def buildCalendarICS() -> ics.icalendar.Calendar:
    calendar =  ics.icalendar.Calendar(creator=ICS_AUTHOR)
    for year in range(2018, datetime.datetime.now().year+2):
        for event in parseCalendarJSON(loadCalendarJSON(year)):
            calendar.events.add(event)
    return calendar

def main():
    calendar = buildCalendarICS()
    with open(ICS_FILE_OUTPUT_PATH, 'w') as icsFile:
        icsFile.writelines(calendar.serialize_iter())

main()