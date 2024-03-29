from datetime import timedelta

refreshTokenURL = "https://oauth2.googleapis.com/token?access_type=offline&refresh_token={refreshToken}&client_id={clientId}&client_secret={clientSecret}&grant_type=refresh_token"
googleSheetURL = "https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{sheetName}!{range}?{options}"

sheetId = "11nXeAZFCJHVirQOwQqVtjK2g4TExwcAjOJhjw27uLs8"
sheetName = "Attendance"

googleCalendarURL = "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events/{eventId}?{options}"

calendarId = "75bcdf66f88e9f2cc153ddce0f6f4a8c6a98ef9517b33d8fb57a7d54e7d34658@group.calendar.google.com"

dateFormat = "%d/%m/%Y %H.%M.%S"

defaultEquipment = "Pinne/Monopinna, Pinnette/Monino, Boccaglio"

googleCredentialsPath = "../data/google_credentials.json"

noticeTime = timedelta(hours=1)

loggerPath = "../data/logs.log"