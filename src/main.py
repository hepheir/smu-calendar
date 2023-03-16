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
        ics_properties = {
            'name' : eventJSON["articleTitle"],
            'begin' : cvtStr2Datetime(eventJSON["etcChar6"]),
            'end' : cvtStr2Datetime(eventJSON["etcChar7"]),
            'uid' : str(eventJSON["articleNo"]),
            'description' : eventJSON["articleText"],
            'created' : cvtInt2Datetime(eventJSON["createDt"]),
            'last_modified' : cvtInt2Datetime(eventJSON["updateDt"]),
            'url' : "https://www.smu.ac.kr/ko/life/academicCalendar.do", # smu.ac.kr 학사일정 페이지 URL
        }

        # XXX:
        #   일부 이벤트는 시작일이 종료일보다 먼저라서 오류로 추가가 되지 않음.
        #   그러나, 학교 홈페이지 학사일정 상에는 당일 이벤트로 올라와 있는 경우가 있음.
        #   당일 일정이므로 종료일에 시작일을 대입하여 임시 방편으로 예외처리 해두었으나, 좋은 방법은 아닌 것 같음.
        #   추후 수정 요함.
        if ics_properties['end'] < ics_properties['begin']:
            ics_properties['end'] = ics_properties['begin']

        try:
            event = ics.event.Event(**ics_properties)
            event.make_all_day()
            yield event
        except:
            print('[WARN] Failed to add an ics event:')
            print(f'    name: {eventJSON["articleTitle"]}')
            print(f'    begin: {cvtStr2Datetime(eventJSON["etcChar6"])}')
            print(f'    end: {cvtStr2Datetime(eventJSON["etcChar7"])}')
            print(f'    uid: {str(eventJSON["articleNo"])}')
            print(f'    created: {cvtInt2Datetime(eventJSON["createDt"])}')
            print(f'    last_modified: {cvtInt2Datetime(eventJSON["updateDt"])}')
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