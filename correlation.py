import sqlite3

events = {
    "50 Y Free": 0,
    "100 Y Free": 0,
    "200 Y Free": 0,
    "500 Y Free": 0,
    "1000 Y Free": 0,
    "1650 Y Free": 0,
    "100 Y Back": 0,
    "200 Y Back": 0,
    "100 Y Breast": 0,
    "200 Y Breast": 0,
    "100 Y Fly": 0,
    "200 Y Fly": 0,
    "200 Y IM": 0,
    "400 Y IM": 0,
}

con = sqlite3.connect("correlations.sqlite")
cur = con.cursor()

for key in events:
    primaryEvent = key
    eventTotal = 0

    for row in cur.execute("SELECT * FROM events WHERE primaryEvent = ?", (primaryEvent,)):
        eventTotal += 1

        events[row[1]] = events[row[1]] + 1
        events[row[2]] = events[row[2]] + 1
        events[row[3]] = events[row[3]] + 1

    for key2 in events:
        if (key2 == primaryEvent):
            continue
        else:
            print(f"{primaryEvent} correlation to {key2} {' ' * (12 - len(key2))}: {round(events[key2] / eventTotal, 4)}")

            cur.execute(f'INSERT INTO correlations VALUES ("{primaryEvent}-{key2}", {round(events[key2] / eventTotal, 4) * 10000})')
            print("Inserted into database")

    events = {
        "50 Y Free": 0,
        "100 Y Free": 0,
        "200 Y Free": 0,
        "500 Y Free": 0,
        "1000 Y Free": 0,
        "1650 Y Free": 0,
        "100 Y Back": 0,
        "200 Y Back": 0,
        "100 Y Breast": 0,
        "200 Y Breast": 0,
        "100 Y Fly": 0,
        "200 Y Fly": 0,
        "200 Y IM": 0,
        "400 Y IM": 0,
    }

con.commit()
con.close()