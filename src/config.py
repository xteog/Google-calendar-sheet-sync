refreshTokenURL = "https://oauth2.googleapis.com/token?access_type=offline&refresh_token={refreshToken}&client_id={clientId}&client_secret={clientSecret}&grant_type=refresh_token"
googleSheetURL = "https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{sheetName}!{range}:{resource}?{options}"

sheetId = 0
sheetName = 0

googleCalendarURL = "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events/{eventId}"

calendarId = "75bcdf66f88e9f2cc153ddce0f6f4a8c6a98ef9517b33d8fb57a7d54e7d34658@group.calendar.google.com"

dateTimeFormat = "%Y/%m/%d %H:%M:%S"

defaultEquipment = "None"

googleCredentialsPath = "../data/google_credentials.json"

